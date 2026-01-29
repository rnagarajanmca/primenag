import { useEffect, useMemo, useRef, useState } from 'react'
import type { RefObject } from 'react'
import './App.css'

type Parameter = {
  name: string
  type: string
  description: string
  default?: unknown
}

type VisualizationHint = {
  mode: string
  steps?: string
  sample_input?: Record<string, unknown>
}

type AlgorithmMeta = {
  name: string
  category: string
  summary: string
  description: string
  complexity: string
  references: string[]
  parameters: Parameter[]
  visualization?: VisualizationHint
}

type SampleRun = {
  input: Record<string, unknown>
  output: Record<string, unknown>
}

type VisualizationData =
  | { kind: 'list'; values: number[] }
  | { kind: 'metrics'; entries: { label: string; value: number }[] }
  | null

const TABS = ['Overview', 'Docs', 'Visualization'] as const

function App() {
  const [algorithms, setAlgorithms] = useState<AlgorithmMeta[]>([])
  const [selected, setSelected] = useState<AlgorithmMeta | null>(null)
  const [activeTab, setActiveTab] = useState<(typeof TABS)[number]>('Overview')
  const [sample, setSample] = useState<SampleRun | null>(null)
  const [vizData, setVizData] = useState<VisualizationData>(null)
  const [error, setError] = useState<string | null>(null)
  const canvasRef = useRef<HTMLCanvasElement | null>(null)

  useEffect(() => {
    fetch('/algorithms.json')
      .then((res) => {
        if (!res.ok) throw new Error('Failed to load algorithms.json')
        return res.json()
      })
      .then((data: AlgorithmMeta[]) => {
        setAlgorithms(data)
        setSelected((prev) => prev ?? data[0] ?? null)
      })
      .catch((err) => setError(err.message))
  }, [])

  useEffect(() => {
    if (!selected) {
      setSample(null)
      setVizData(null)
      return
    }

    const examplePath = `/examples/${selected.name}.json`
    fetch(examplePath)
      .then((res) => {
        if (!res.ok) throw new Error('no-sample')
        return res.json()
      })
      .then((data: SampleRun) => {
        setSample(data)
        setVizData(extractVisualizationData(data))
      })
      .catch(() => {
        setSample(null)
        setVizData(null)
      })
  }, [selected])

  useEffect(() => {
    if (!selected || activeTab !== 'Visualization') return
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.fillStyle = '#0f172a'
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    ctx.fillStyle = '#facc15'
    ctx.font = '16px "Space Grotesk", sans-serif'
    ctx.fillText(`Visualization hint: ${selected.visualization?.mode ?? 'N/A'}`, 16, 32)

    if (selected.visualization?.steps) {
      wrapText(ctx, selected.visualization.steps, 16, 60, canvas.width - 32, 20)
    } else {
      ctx.fillText('No steps provided. Add visualization metadata to see more.', 16, 60)
    }
    if (vizData?.kind === 'list') {
      drawList(ctx, vizData.values, canvas)
    } else if (vizData?.kind === 'metrics') {
      drawMetrics(ctx, vizData.entries, canvas)
    }
  }, [selected, activeTab, vizData])

  const grouped = useMemo(() => {
    return algorithms.reduce<Record<string, AlgorithmMeta[]>>((acc, meta) => {
      const key = meta.category
      acc[key] = acc[key] ?? []
      acc[key].push(meta)
      return acc
    }, {})
  }, [algorithms])

  if (error) {
    return (
      <div className="app">
        <div className="error-banner">Failed to load metadata: {error}</div>
      </div>
    )
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <h1>PrimeNag</h1>
        <p className="sidebar-subtitle">Select an algorithm to inspect.</p>
        <div className="sidebar-list">
          {Object.entries(grouped).map(([category, metas]) => (
            <div key={category} className="sidebar-section">
              <p className="sidebar-section-title">{category}</p>
              {metas.map((meta) => (
                <button
                  key={meta.name}
                  className={`sidebar-item ${
                    selected?.name === meta.name ? 'active' : ''
                  }`}
                  onClick={() => {
                    setSelected(meta)
                    setActiveTab('Overview')
                  }}
                >
                  <span className="item-name">{meta.name}</span>
                  <span className="item-summary">{meta.summary}</span>
                </button>
              ))}
            </div>
          ))}
        </div>
      </aside>

      <main className="content">
        {selected ? (
          <>
            <header className="content-header">
              <div>
                <p className="eyebrow">{selected.category}</p>
                <h2>{selected.name}</h2>
                <p className="summary">{selected.summary}</p>
              </div>
              <div className="chip">Complexity: {selected.complexity}</div>
            </header>

            <div className="tabs">
              {TABS.map((tab) => (
                <button
                  key={tab}
                  className={`tab ${activeTab === tab ? 'active' : ''}`}
                  onClick={() => setActiveTab(tab)}
                >
                  {tab}
                </button>
              ))}
            </div>

            <section className="tab-panel">
              {activeTab === 'Overview' && (
                <OverviewTab meta={selected} />
              )}
              {activeTab === 'Docs' && (
                <DocsTab meta={selected} />
              )}
              {activeTab === 'Visualization' && (
                <VisualizationTab
                  meta={selected}
                  sample={sample}
                  vizData={vizData}
                  canvasRef={canvasRef}
                />
              )}
            </section>
          </>
        ) : (
          <div className="empty-state">Loading metadata…</div>
        )}
      </main>
    </div>
  )
}

function OverviewTab({ meta }: { meta: AlgorithmMeta }) {
  return (
    <div className="panel-body">
      <h3>Parameters</h3>
      {meta.parameters.length === 0 && <p>No parameters documented.</p>}
      <ul className="parameter-list">
        {meta.parameters.map((param) => (
          <li key={param.name}>
            <strong>{param.name}</strong>
            <span className="type">{param.type}</span>
            <p>{param.description}</p>
            {param.default !== undefined && (
              <small>Default: {String(param.default)}</small>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}

function DocsTab({ meta }: { meta: AlgorithmMeta }) {
  return (
    <div className="panel-body">
      <h3>Description</h3>
      <p>{meta.description}</p>
      {meta.references.length > 0 && (
        <>
          <h3>References</h3>
          <ul>
            {meta.references.map((ref) => (
              <li key={ref}>
                <a href={ref} target="_blank" rel="noreferrer">
                  {ref}
                </a>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  )
}

function VisualizationTab({
  meta,
  sample,
  vizData,
  canvasRef,
}: {
  meta: AlgorithmMeta
  sample: SampleRun | null
  vizData: VisualizationData
  canvasRef: RefObject<HTMLCanvasElement | null>
}) {
  return (
    <div className="panel-body visualization">
      <div className="canvas-wrapper">
        <canvas ref={canvasRef} width={800} height={260} />
      </div>
      <div className="viz-details">
        <h3>Instructions</h3>
        <p>{meta.visualization?.steps ?? 'No visualization instructions yet.'}</p>
        {vizData?.kind === 'list' && (
          <p className="viz-hint">
            Rendering first {vizData.values.length} values from sample output.
          </p>
        )}
        {vizData?.kind === 'metrics' && (
          <p className="viz-hint">Comparing analytic estimates against actuals.</p>
        )}
        {sample && (
          <>
            <h4>Sample Input</h4>
            <pre>{JSON.stringify(sample.input, null, 2)}</pre>
            <h4>Sample Output</h4>
            <pre>{JSON.stringify(sample.output, null, 2)}</pre>
          </>
        )}
        {!sample && <p>No sample output available.</p>}
      </div>
    </div>
  )
}

function wrapText(
  ctx: CanvasRenderingContext2D,
  text: string,
  x: number,
  y: number,
  maxWidth: number,
  lineHeight: number,
) {
  const words = text.split(' ')
  let line = ''
  for (const word of words) {
    const testLine = `${line}${word} `
    const metrics = ctx.measureText(testLine)
    if (metrics.width > maxWidth && line !== '') {
      ctx.fillText(line, x, y)
      line = `${word} `
      y += lineHeight
    } else {
      line = testLine
    }
  }
  ctx.fillText(line, x, y)
}

function extractVisualizationData(sample: SampleRun): VisualizationData {
  const result = sample.output?.result
  if (Array.isArray(result)) {
    const numericValues = result
      .map((value) => Number(value))
      .filter((value) => Number.isFinite(value))
    if (numericValues.length) {
      return { kind: 'list', values: numericValues.slice(0, 40) }
    }
  }

  if (
    result &&
    typeof result === 'object' &&
    'actual' in result &&
    'pnt' in result &&
    'li' in result
  ) {
    return {
      kind: 'metrics',
      entries: [
        { label: 'π(n)', value: Number((result as Record<string, unknown>).actual) },
        { label: 'n / ln n', value: Number((result as Record<string, unknown>).pnt) },
        { label: 'Li(n)', value: Number((result as Record<string, unknown>).li) },
      ].filter((entry) => Number.isFinite(entry.value)),
    }
  }

  return null
}

function drawList(
  ctx: CanvasRenderingContext2D,
  values: number[],
  canvas: HTMLCanvasElement,
) {
  if (!values.length) return
  const max = Math.max(...values)
  const barWidth = (canvas.width - 32) / values.length
  ctx.fillStyle = '#0ea5e9'
  values.forEach((value, idx) => {
    const height = (value / max) * (canvas.height - 80)
    ctx.fillRect(
      16 + idx * barWidth,
      canvas.height - 20 - height,
      Math.max(barWidth - 4, 2),
      height,
    )
  })
}

function drawMetrics(
  ctx: CanvasRenderingContext2D,
  entries: { label: string; value: number }[],
  canvas: HTMLCanvasElement,
) {
  if (!entries.length) return
  const max = Math.max(...entries.map((entry) => entry.value))
  const width = canvas.width - 32
  entries.forEach((entry, idx) => {
    const y = 120 + idx * 50
    const ratio = entry.value / max || 0
    ctx.fillStyle = '#475569'
    ctx.fillRect(16, y, width, 24)
    ctx.fillStyle = '#facc15'
    ctx.fillRect(16, y, width * ratio, 24)
    ctx.fillStyle = '#cbd5f5'
    ctx.fillText(`${entry.label}: ${entry.value.toFixed(2)}`, 16, y - 8)
  })
}

export default App

