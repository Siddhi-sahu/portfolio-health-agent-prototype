import React, { useEffect, useMemo, useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const riskOrder = {
  HIGH: 0,
  MEDIUM: 1,
  LOW: 2,
};

const riskLabels = {
  HIGH: "High",
  MEDIUM: "Medium",
  LOW: "Low",
};

const feedbackDecisions = ["APPROVED", "REJECTED", "NEEDS_MORE_INFO"];

function formatCurrency(value) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value || 0);
}

function formatPercent(value) {
  return `${Math.round((value || 0) * 100)}%`;
}

function App() {
  const [autonomyLevel, setAutonomyLevel] = useState(1);
  const [portfolio, setPortfolio] = useState(null);
  const [summary, setSummary] = useState(null);
  const [activityLogs, setActivityLogs] = useState([]);
  const [officerFeedback, setOfficerFeedback] = useState([]);
  const [selectedLoanIndex, setSelectedLoanIndex] = useState(0);
  const [feedbackDecision, setFeedbackDecision] = useState("APPROVED");
  const [feedbackNotes, setFeedbackNotes] = useState("");
  const [status, setStatus] = useState("Loading portfolio data");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const analyses = useMemo(() => {
    const items = portfolio?.portfolioAnalysis || [];
    return [...items].sort((a, b) => {
      return riskOrder[a.analysis.riskLevel] - riskOrder[b.analysis.riskLevel];
    });
  }, [portfolio]);

  const selectedItem = useMemo(() => {
    return analyses[selectedLoanIndex] || analyses[0];
  }, [analyses, selectedLoanIndex]);

  const metrics = useMemo(() => {
    const total = analyses.length || 1;
    const counts = analyses.reduce(
      (acc, item) => {
        acc[item.analysis.riskLevel] += 1;
        return acc;
      },
      { HIGH: 0, MEDIUM: 0, LOW: 0 }
    );

    const exposure = analyses.reduce((sum, item) => sum + item.loan.loanAmount, 0);
    const delinquent = analyses.reduce((sum, item) => sum + item.loan.delinquentAmount, 0);
    const autoHandled = analyses.filter((item) => item.analysis.automatedDecision).length;
    const reviewRequired = analyses.filter(
      (item) => item.analysis.autonomyPolicy !== "AUTO_HANDLE"
    ).length;

    return {
      counts,
      total,
      exposure,
      delinquent,
      autoHandled,
      reviewRequired,
    };
  }, [analyses]);

  useEffect(() => {
    loadDashboard();
  }, [autonomyLevel]);

  async function requestJson(path, options) {
    const response = await fetch(`${API_BASE_URL}${path}`, options);

    if (!response.ok) {
      throw new Error(`${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async function loadDashboard() {
    setError("");
    setStatus("Refreshing portfolio intelligence");

    try {
      const [portfolioData, summaryData, logsData, feedbackData] = await Promise.all([
        requestJson(`/portfolio-analysis?autonomy_level=${autonomyLevel}`),
        requestJson("/portfolio-summary"),
        requestJson("/activity-logs"),
        requestJson("/officer-feedback"),
      ]);

      setPortfolio(portfolioData);
      setSummary(summaryData);
      setActivityLogs(logsData.logs || []);
      setOfficerFeedback(feedbackData.feedback || []);
      setSelectedLoanIndex(0);
      setStatus("Live data connected");
    } catch (err) {
      setError(`Could not connect to backend at ${API_BASE_URL}. ${err.message}`);
      setStatus("Backend connection needed");
    }
  }

  async function submitFeedback(event) {
    event.preventDefault();

    if (!selectedItem || !feedbackNotes.trim()) {
      return;
    }

    setIsSubmitting(true);
    setError("");

    try {
      await requestJson("/officer-feedback", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          client: selectedItem.analysis.client,
          decision: feedbackDecision,
          notes: feedbackNotes.trim(),
        }),
      });

      setFeedbackNotes("");
      const feedbackData = await requestJson("/officer-feedback");
      setOfficerFeedback(feedbackData.feedback || []);
      setStatus("Officer feedback captured");
    } catch (err) {
      setError(`Could not submit officer feedback. ${err.message}`);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Mifos X prototype</p>
          <h1>Portfolio Health Agent</h1>
        </div>
        <div className="connection-block">
          <span className={`status-dot ${error ? "offline" : "online"}`} />
          <span>{status}</span>
          <button className="icon-button" type="button" onClick={loadDashboard} aria-label="Refresh dashboard">
            R
          </button>
        </div>
      </header>

      {error && <div className="notice">{error}</div>}

      <section className="control-strip">
        <div>
          <p className="section-kicker">Autonomy level</p>
          <h2>Governed agent policy</h2>
        </div>
        <div className="segmented-control" aria-label="Autonomy level">
          {[1, 2, 3].map((level) => (
            <button
              key={level}
              className={autonomyLevel === level ? "active" : ""}
              type="button"
              onClick={() => setAutonomyLevel(level)}
            >
              Level {level}
            </button>
          ))}
        </div>
      </section>

      <section className="metric-grid">
        <Metric label="Total loans" value={portfolio?.totalLoans || 0} />
        <Metric label="High risk" value={metrics.counts.HIGH} tone="danger" />
        <Metric label="Needs review" value={metrics.reviewRequired} tone="warning" />
        <Metric label="Auto handled" value={metrics.autoHandled} tone="success" />
        <Metric label="Exposure" value={formatCurrency(metrics.exposure)} />
        <Metric label="Delinquent" value={formatCurrency(metrics.delinquent)} tone="danger" />
      </section>

      <section className="dashboard-grid">
        <div className="panel table-panel">
          <div className="panel-heading">
            <div>
              <p className="section-kicker">Risk queue</p>
              <h2>Loan decisions</h2>
            </div>
            <span>{summary?.portfolioHealth || "Pending"}</span>
          </div>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Client</th>
                  <th>Risk</th>
                  <th>Score</th>
                  <th>Policy</th>
                  <th>Approval</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                  {analyses.map((item, index) => (
                  <tr
                    key={`${item.analysis.client}-${index}`}
                    className={selectedLoanIndex === index ? "selected" : ""}
                    onClick={() => setSelectedLoanIndex(index)}
                  >
                    <td>
                      <strong>{item.analysis.client}</strong>
                      <span>{item.loan.loanStatus}</span>
                    </td>
                    <td>
                      <RiskBadge risk={item.analysis.riskLevel} />
                    </td>
                    <td>{item.analysis.riskScore}</td>
                    <td>{item.analysis.autonomyPolicy}</td>
                    <td>{item.analysis.approvalStatus}</td>
                    <td>{item.analysis.suggestedAction}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <aside className="panel detail-panel">
          <div className="panel-heading">
            <div>
              <p className="section-kicker">Explainability</p>
              <h2>{selectedItem?.analysis.client || "Select a client"}</h2>
            </div>
            {selectedItem && <RiskBadge risk={selectedItem.analysis.riskLevel} />}
          </div>

          {selectedItem ? (
            <>
              <div className="confidence-block">
                <div>
                  <span>Deterministic confidence</span>
                  <strong>{formatPercent(selectedItem.analysis.confidenceScore)}</strong>
                </div>
                <div className="confidence-track">
                  <span style={{ width: `${Math.min(selectedItem.analysis.confidenceScore * 100, 100)}%` }} />
                </div>
              </div>

              <div className="factor-list">
                {selectedItem.analysis.decisionFactors.map((factor) => (
                  <div className="factor-row" key={factor.factor}>
                    <div>
                      <strong>{factor.factor}</strong>
                      <span>{String(factor.value)}</span>
                    </div>
                    <ImpactBar impact={factor.impact} />
                    <b>{factor.impact}</b>
                  </div>
                ))}
              </div>

              <div className="explanation-list">
                {selectedItem.analysis.explanation.map((text) => (
                  <p key={text}>{text}</p>
                ))}
              </div>
            </>
          ) : (
            <p className="empty-state">Run the backend to load portfolio decisions.</p>
          )}
        </aside>
      </section>

      <section className="dashboard-grid lower-grid">
        <div className="panel">
          <div className="panel-heading">
            <div>
              <p className="section-kicker">Human oversight</p>
              <h2>Officer feedback</h2>
            </div>
          </div>
          <form className="feedback-form" onSubmit={submitFeedback}>
            <label>
              Client
              <select value={selectedLoanIndex} onChange={(event) => setSelectedLoanIndex(Number(event.target.value))}>
                {analyses.map((item, index) => (
                  <option key={`${item.analysis.client}-${index}`} value={index}>
                    {item.analysis.client} - {item.analysis.riskLevel}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Decision
              <select value={feedbackDecision} onChange={(event) => setFeedbackDecision(event.target.value)}>
                {feedbackDecisions.map((decision) => (
                  <option key={decision} value={decision}>
                    {decision}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Notes
              <textarea
                value={feedbackNotes}
                onChange={(event) => setFeedbackNotes(event.target.value)}
                placeholder="Document the officer judgement for audit and trust evaluation."
              />
            </label>
            <button className="primary-button" type="submit" disabled={!selectedItem || !feedbackNotes.trim() || isSubmitting}>
              {isSubmitting ? "Submitting" : "Submit feedback"}
            </button>
          </form>
        </div>

        <div className="panel">
          <div className="panel-heading">
            <div>
              <p className="section-kicker">Governance trail</p>
              <h2>Recent records</h2>
            </div>
          </div>
          <div className="record-list">
            {officerFeedback.slice(-4).reverse().map((entry) => (
              <Record
                key={`${entry.timestamp}-${entry.client}`}
                title={`${entry.client} - ${entry.decision}`}
                detail={entry.notes}
                meta={new Date(entry.timestamp).toLocaleString()}
              />
            ))}
            {activityLogs.slice(-4).reverse().map((entry) => (
              <Record
                key={`${entry.timestamp}-${entry.client}-${entry.action}`}
                title={`${entry.client} - ${entry.action}`}
                detail={`${entry.riskLevel} risk, ${entry.status}`}
                meta={new Date(entry.timestamp).toLocaleString()}
              />
            ))}
            {!officerFeedback.length && !activityLogs.length && (
              <p className="empty-state">Decision and feedback records will appear here.</p>
            )}
          </div>
        </div>
      </section>
    </main>
  );
}

function Metric({ label, value, tone = "neutral" }) {
  return (
    <div className={`metric ${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function RiskBadge({ risk }) {
  return <span className={`risk-badge ${risk.toLowerCase()}`}>{riskLabels[risk] || risk}</span>;
}

function ImpactBar({ impact }) {
  return (
    <div className="impact-track" aria-label={`Impact ${impact}`}>
      <span style={{ width: `${Math.min((impact / 50) * 100, 100)}%` }} />
    </div>
  );
}

function Record({ title, detail, meta }) {
  return (
    <article className="record-item">
      <strong>{title}</strong>
      <span>{detail}</span>
      <time>{meta}</time>
    </article>
  );
}

export default App;
