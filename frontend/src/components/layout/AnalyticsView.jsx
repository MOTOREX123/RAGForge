import { TrendingUp, MessageSquare, Clock, Database, BrainCircuit, Zap, CheckCircle, AlertCircle, Server } from "lucide-react";

export function AnalyticsView() {
  // In a real app, these would come from the backend
  // For now, we show a clear "Demo UI" notice since the backend doesn't provide analytics yet
  const demoMetrics = {
    totalQueries: 142,
    localQueries: 89,
    webQueries: 43,
    generalQueries: 10,
    avgResponseTime: 2.3,
    avgCitationsPerResponse: 2.4,
    topDocuments: [
      { name: "DeepLearning.pdf", queries: 34, avgScore: 0.82 },
      { name: "AI & ML DIGITAL NOTES.pdf", queries: 28, avgScore: 0.76 },
      { name: "Introduction to Machine Learning with Python.pdf", queries: 22, avgScore: 0.71 },
      { name: "IntroductiontoAgenticAI.pdf", queries: 15, avgScore: 0.68 },
    ],
    queriesByDay: [
      { day: "Mon", count: 12 },
      { day: "Tue", count: 18 },
      { day: "Wed", count: 24 },
      { day: "Thu", count: 19 },
      { day: "Fri", count: 31 },
      { day: "Sat", count: 22 },
      { day: "Sun", count: 16 },
    ],
    providerStatus: {
      ollama: { status: "healthy", uptime: "99.2%", avgLatency: "1.2s" },
      openrouter: { status: "healthy", uptime: "99.8%", avgLatency: "0.8s" },
      gemini: { status: "healthy", uptime: "98.5%", avgLatency: "1.5s" },
    },
  };

  const statCards = [
    {
      icon: MessageSquare,
      label: "Total Queries",
      value: demoMetrics.totalQueries,
      change: "+12%",
      trend: "up",
    },
    {
      icon: BrainCircuit,
      label: "Local RAG Queries",
      value: demoMetrics.localQueries,
      change: "62.7% of total",
      trend: "neutral",
    },
    {
      icon: Zap,
      label: "Avg Response Time",
      value: `${demoMetrics.avgResponseTime}s`,
      change: "-0.3s vs last week",
      trend: "up",
    },
    {
      icon: Database,
      label: "Avg Citations/Response",
      value: demoMetrics.avgCitationsPerResponse,
      change: "Target: ≥2",
      trend: "up",
    },
  ];

  return (
    <div className="flex h-full flex-col bg-bg">
      {/* Header */}
      <div className="border-b border-line px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <img
              src="/assets/ragforge-logo.png"
              alt="RAGForge"
              className="w-6 h-6"
            />
            <div>
              <h1 className="font-display text-lg font-semibold text-ink">Analytics</h1>
              <p className="text-[11px] text-ink-muted">Usage metrics and performance insights</p>
            </div>
          </div>
          <div className="flex items-center gap-1.5 rounded-lg border border-line bg-surface px-2.5 py-1.5 text-[10px] text-ink-muted">
            <AlertCircle size={11} className="text-purple" />
            Demo data — backend analytics not yet implemented
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto px-4 py-4">
        <div className="w-full space-y-4">
          {/* Demo Notice */}
          <div className="rounded-lg border border-purple/30 bg-purple-bg p-3">
            <div className="flex items-start gap-2.5">
              <AlertCircle size={18} className="shrink-0 text-purple" />
              <div>
                <h3 className="font-medium text-purple">Analytics Dashboard (Demo Mode)</h3>
                <p className="mt-1 text-sm text-ink-muted">
                  The backend does not currently expose analytics endpoints. The charts and metrics
                  below are <strong>simulated demo data</strong> for UI demonstration purposes only.
                  Real analytics would require backend implementation of query logging, metrics
                  aggregation, and a dedicated <code className="font-mono text-[10px] bg-bg px-1 rounded">/api/analytics</code> endpoint.
                </p>
              </div>
            </div>
          </div>

          {/* Stat Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {statCards.map((stat) => (
              <StatCard key={stat.label} {...stat} />
            ))}
          </div>

          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {/* Query Volume */}
            <ChartCard title="Query Volume (Last 7 Days)" icon={TrendingUp}>
              <QueryVolumeChart data={demoMetrics.queriesByDay} />
            </ChartCard>

            {/* Query Distribution */}
            <ChartCard title="Query Distribution by Route" icon={BrainCircuit}>
              <QueryDistributionChart
                local={demoMetrics.localQueries}
                web={demoMetrics.webQueries}
                general={demoMetrics.generalQueries}
              />
            </ChartCard>
          </div>

          {/* Top Documents & Provider Status */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <ChartCard title="Top Referenced Documents" icon={Database}>
              <TopDocumentsTable documents={demoMetrics.topDocuments} />
            </ChartCard>

            <ChartCard title="Provider Health" icon={Server}>
              <ProviderStatusTable providers={demoMetrics.providerStatus} />
            </ChartCard>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, change, trend }) {
  const trendColors = {
    up: "text-green",
    down: "text-red",
    neutral: "text-ink-muted",
  };

  return (
    <div className="rounded-lg border border-line bg-surface p-4">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-ink-muted">{label}</p>
          <p className="mt-0.5 font-display text-xl font-semibold text-ink">{value}</p>
        </div>
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-purple-bg text-purple">
          <Icon size={18} strokeWidth={2} />
        </div>
      </div>
      <p className={`mt-2 text-[10px] font-medium ${trendColors[trend]}`}>
        {change}
      </p>
    </div>
  );
}

function ChartCard({ title, icon: Icon, children }) {
  return (
    <div className="rounded-lg border border-line bg-surface p-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-1.5">
          <Icon size={16} className="text-purple" />
          <h3 className="font-display text-sm font-semibold text-ink">{title}</h3>
        </div>
      </div>
      <div className="h-56">{children}</div>
    </div>
  );
}

function QueryVolumeChart({ data }) {
  const maxCount = Math.max(...data.map((d) => d.count));
  const barHeight = 180;

  return (
    <div className="h-full flex items-end justify-center gap-2 px-2">
      {data.map((d) => (
        <div key={d.day} className="flex flex-col items-center gap-1.5 flex-1">
          <div
            className="w-full rounded-t bg-purple-bg transition-all hover:bg-purple/20"
            style={{
              height: `${(d.count / maxCount) * barHeight}px`,
              minHeight: "4px",
            }}
          />
          <span className="text-[10px] text-ink-muted">{d.day}</span>
          <span className="font-mono text-[10px] text-ink">{d.count}</span>
        </div>
      ))}
    </div>
  );
}

function QueryDistributionChart({ local, web, general }) {
  const total = local + web + general;
  const segments = [
    { value: local, color: "#7C5CFF", label: "Local", count: local },
    { value: web, color: "#10B981", label: "Web", count: web },
    { value: general, color: "#6B7280", label: "General", count: general },
  ].filter((s) => s.value > 0);

  return (
    <div className="h-full flex flex-col items-center justify-center gap-3 px-3">
      <div className="relative w-40 h-40">
        <svg viewBox="0 0 100 100" className="w-full h-full -rotate-90">
          <circle
            cx="50"
            cy="50"
            r="40"
            fill="none"
            stroke="rgba(139, 148, 158, 0.12)"
            strokeWidth="16"
          />
          {segments.map((segment, index) => {
            const previous = segments.slice(0, index).reduce((sum, s) => sum + s.value, 0);
            const offset = (previous / total) * 251.2; // 2 * PI * 40
            const length = (segment.value / total) * 251.2;
            return (
              <circle
                key={segment.label}
                cx="50"
                cy="50"
                r="40"
                fill="none"
                stroke={segment.color}
                strokeWidth="16"
                strokeDasharray={`${length} 251.2`}
                strokeDashoffset={offset}
                strokeLinecap="round"
                className="transition-all duration-500"
              />
            );
          })}
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <p className="font-display text-lg font-bold text-ink">{total}</p>
            <p className="text-[10px] text-ink-muted">Total</p>
          </div>
        </div>
      </div>
      <div className="flex flex-wrap items-center justify-center gap-3">
        {segments.map((segment) => (
          <div key={segment.label} className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded" style={{ backgroundColor: segment.color }} />
            <span className="text-sm text-ink">
              {segment.label} ({Math.round((segment.value / total) * 100)}%)
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

function TopDocumentsTable({ documents }) {
  return (
    <div className="h-full overflow-y-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-line">
            <th className="text-left pb-2 font-medium text-ink-muted">Document</th>
            <th className="text-right pb-2 font-medium text-ink-muted">Queries</th>
            <th className="text-right pb-2 font-medium text-ink-muted">Avg Score</th>
          </tr>
        </thead>
        <tbody>
          {documents.map((doc, index) => (
            <tr key={doc.name} className="border-b border-line/50">
              <td className="py-2">
                <div className="flex items-center gap-1.5">
                  <span className="font-mono text-[10px] text-ink-muted">{index + 1}.</span>
                  <span className="truncate max-w-[200px] text-ink">{doc.name}</span>
                </div>
              </td>
              <td className="py-2 text-right font-mono text-ink">{doc.queries}</td>
              <td className="py-2 text-right">
                <span className={`font-mono ${doc.avgScore > 0.75 ? "text-green" : "text-ink"}`}>
                  {Math.round(doc.avgScore * 100)}%
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ProviderStatusTable({ providers }) {
  const statusConfig = {
    healthy: { icon: CheckCircle, color: "text-green", label: "Healthy" },
    degraded: { icon: AlertCircle, color: "text-yellow", label: "Degraded" },
    down: { icon: AlertCircle, color: "text-red", label: "Down" },
  };

  return (
    <div className="h-full space-y-2.5">
      {Object.entries(providers).map(([key, provider]) => {
        const config = statusConfig[provider.status] || statusConfig.degraded;
        const Icon = config.icon;

        return (
          <div key={key} className="flex items-center justify-between p-2.5 rounded-lg border border-line bg-raised/50">
            <div className="flex items-center gap-2.5">
              <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-purple-bg text-purple">
                <Server size={14} />
              </div>
              <div>
                <p className="font-medium text-ink capitalize">{key}</p>
                <p className="text-[10px] text-ink-muted">
                  {provider.avgLatency} avg latency · {provider.uptime} uptime
                </p>
              </div>
            </div>
            <div className="flex items-center gap-1.5">
              <Icon size={12} className={config.color} />
              <span className={`text-sm font-medium ${config.color}`}>
                {config.label}
              </span>
            </div>
          </div>
        );
      })}
    </div>
  );
}