
import { useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

const FEATURES = {
    analyze: {
        title: "Email Status Intelligence",
        description: "Discover what the email means and what you should do next.",
        button: "Analyze Email",
        endpoint: "/api/analyze-email",
    },
    summarize: {
        title: "Email Summary",
        description: "Understand the key information in an email.",
        button: "Summarize Email",
        endpoint: "/api/summarize-email",
    },
    classify: {
        title: "Email Classification",
        description: "Identify the primary category of an email.",
        button: "Classify Email",
        endpoint: "/api/classify-email",
    },
    actions: {
        title: "Extract Action Items",
        description: "Find tasks, deadlines, and responsible people.",
        button: "Extract Action Items",
        endpoint: "/api/extract-action",
    },
    reply: {
        title: "Generate a Reply",
        description: "Draft a reply using your preferred tone.",
        button: "Generate Reply",
        endpoint: "/api/generate-reply",
    },
};

function App() {
    const [activeTab, setActiveTab] = useState("analyze");

    const [email, setEmail] = useState({
        sender: "",
        recipient: "",
        subject: "",
        body: "",
    });

    const [tone, setTone] = useState("Professional");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const feature = FEATURES[activeTab];

    function handleEmailChange(event) {
        const { name, value } = event.target;

        setEmail((previousEmail) => ({
            ...previousEmail,
            [name]: value,
        }));
    }

    function handleTabChange(tab) {
        setActiveTab(tab);
        setResult(null);
        setError("");
    }

    async function handleSubmit(event) {
        event.preventDefault();

        setLoading(true);
        setError("");
        setResult(null);

        let requestBody = email;

        if (activeTab === "reply") {
            requestBody = {
                email,
                tone,
            };
        }

        try {
            const response = await fetch(
                `${API_BASE_URL}${feature.endpoint}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Accept: "application/json",
                    },
                    body: JSON.stringify(requestBody),
                }
            );

            const data = await response.json();

            if (!response.ok) {
                const message = Array.isArray(data.detail)
                    ? data.detail.map((item) => item.msg).join(", ")
                    : data.detail || "The request could not be completed.";

                throw new Error(message);
            }

            setResult(data);
        } catch (err) {
            setError(
                err.message ||
                "Could not connect to FastAPI. Check that the backend is running."
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="app">
            <header className="app-header">
                <div className="brand">
                    <div className="brand-icon">AI</div>
                    <div>
                        <h1>AI Email Assistant</h1>
                        <p>Work smarter with your emails</p>
                    </div>
                </div>

                <div className="status">
                    <span className="status-dot"></span>
                    Local AI Assistant
                </div>
            </header>

            <main className="main-content">
                <section className="welcome">
                    <p className="eyebrow">
                        YOUR PERSONAL EMAIL WORKSPACE
                    </p>

                    <h2>Make every email easier.</h2>

                    <p>
                        Understand email status, identify priorities,
                        discover deadlines, and determine your next
                        action with AI-powered email intelligence.
                    </p>
                </section>

                <nav
                    className="tabs"
                    aria-label="Email assistant features"
                >
                    <button
                        type="button"
                        className={activeTab === "analyze" ? "tab active" : "tab"}
                        onClick={() => handleTabChange("analyze")}
                    >
                        Email Intelligence
                    </button>

                    <button
                        type="button"
                        className={activeTab === "summarize" ? "tab active" : "tab"}
                        onClick={() => handleTabChange("summarize")}
                    >
                        Summarize
                    </button>

                    <button
                        type="button"
                        className={activeTab === "classify" ? "tab active" : "tab"}
                        onClick={() => handleTabChange("classify")}
                    >
                        Classify
                    </button>

                    <button
                        type="button"
                        className={activeTab === "actions" ? "tab active" : "tab"}
                        onClick={() => handleTabChange("actions")}
                    >
                        Action Items
                    </button>

                    <button
                        type="button"
                        className={activeTab === "reply" ? "tab active" : "tab"}
                        onClick={() => handleTabChange("reply")}
                    >
                        Generate Reply
                    </button>
                </nav>

                <section className="workspace">
                    <div className="workspace-heading">
                        <div>
                            <h3>{feature.title}</h3>
                            <p>{feature.description}</p>
                        </div>

                        <span className="ai-badge">AI POWERED</span>
                    </div>

                    <form className="email-form" onSubmit={handleSubmit}>
                        <div className="form-row">
                            <div className="form-group">
                                <label htmlFor="sender">Sender Email</label>
                                <input
                                    id="sender"
                                    name="sender"
                                    type="email"
                                    placeholder="sender@example.com"
                                    value={email.sender}
                                    onChange={handleEmailChange}
                                    maxLength={254}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="recipient">Recipient Email</label>
                                <input
                                    id="recipient"
                                    name="recipient"
                                    type="email"
                                    placeholder="recipient@example.com"
                                    value={email.recipient}
                                    onChange={handleEmailChange}
                                    maxLength={254}
                                    required
                                />
                            </div>
                        </div>

                        <div className="form-group">
                            <label htmlFor="subject">Email Subject</label>
                            <input
                                id="subject"
                                name="subject"
                                type="text"
                                placeholder="Enter the email subject"
                                value={email.subject}
                                onChange={handleEmailChange}
                                maxLength={200}
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="body">Email Body</label>
                            <textarea
                                id="body"
                                name="body"
                                placeholder="Paste or type the email content here..."
                                value={email.body}
                                onChange={handleEmailChange}
                                maxLength={20000}
                                rows={8}
                                required
                            />

                            <span className="field-hint">
                                {email.body.length} / 20,000 characters
                            </span>
                        </div>

                        {activeTab === "reply" && (
                            <div className="form-group">
                                <label htmlFor="tone">Reply Tone</label>
                                <select
                                    id="tone"
                                    name="tone"
                                    value={tone}
                                    onChange={(event) => setTone(event.target.value)}
                                >
                                    <option value="Professional">Professional</option>
                                    <option value="Friendly">Friendly</option>
                                    <option value="Concise">Concise</option>
                                </select>
                            </div>
                        )}

                        <button
                            className="submit-button"
                            type="submit"
                            disabled={loading}
                        >
                            {loading ? "Processing..." : feature.button}
                        </button>
                    </form>

                    {error && (
                        <div className="error-message" role="alert">
                            {error}
                        </div>
                    )}

                    {result && activeTab === "analyze" && (
                        <section className="analysis-result" aria-live="polite">
                            <h3>Email Intelligence Results</h3>

                            <div className="result-card">
                                <span className="result-label">Email Status</span>
                                <p className="status-value">{result.email_status}</p>
                            </div>

                            <div className="result-grid">
                                <div className="result-card">
                                    <span className="result-label">Priority</span>
                                    <p>{result.priority}</p>
                                </div>

                                <div className="result-card">
                                    <span className="result-label">Category</span>
                                    <p>{result.category}</p>
                                </div>

                                <div className="result-card">
                                    <span className="result-label">Action Required</span>
                                    <p>{result.action_required ? "Yes" : "No"}</p>
                                </div>
                            </div>

                            <ResultCard label="Email Summary" value={result.summary} />
                            <ResultCard
                                label="Deadline"
                                value={result.deadline || "No explicit deadline identified"}
                            />
                            <ResultCard
                                label="Recommended Next Action"
                                value={result.recommended_action}
                            />
                        </section>
                    )}

                    {result && activeTab === "summarize" && (
                        <section className="analysis-result" aria-live="polite">
                            <h3>Email Summary Result</h3>
                            <ResultCard label="Subject" value={result.subject} />
                            <ResultCard label="Summary" value={result.summary} />
                        </section>
                    )}

                    {result && activeTab === "classify" && (
                        <section className="analysis-result" aria-live="polite">
                            <h3>Classification Result</h3>
                            <ResultCard label="Email Category" value={result.category} />
                        </section>
                    )}

                    {result && activeTab === "actions" && (
                        <section className="analysis-result" aria-live="polite">
                            <h3>Extracted Action Items</h3>

                            {result.action_items?.length > 0 ? (
                                <div className="action-list">
                                    {result.action_items.map((item, index) => (
                                        <div className="result-card result-detail" key={`${item.task}-${index}`}>
                                            <span className="result-label">
                                                Task {index + 1}
                                            </span>
                                            <p>{item.task}</p>
                                            <p>
                                                <strong>Deadline:</strong>{" "}
                                                {item.deadline || "Not specified"}
                                            </p>
                                            <p>
                                                <strong>Assignee:</strong>{" "}
                                                {item.assignee || "Not specified"}
                                            </p>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <ResultCard
                                    label="Result"
                                    value="No action items were identified in this email."
                                />
                            )}
                        </section>
                    )}

                    {result && activeTab === "reply" && (
                        <section className="analysis-result" aria-live="polite">
                            <h3>Generated Reply</h3>
                            <ResultCard label="Reply Subject" value={result.subject} />
                            <ResultCard label="Reply Body" value={result.body} />
                            <ResultCard label="Tone" value={result.tone} />
                        </section>
                    )}
                </section>

                <footer className="app-footer">
                    Powered by React, FastAPI and Ollama
                </footer>
            </main>
        </div>
    );
}

function ResultCard({ label, value }) {
    return (
        <div className="result-card result-detail">
            <span className="result-label">{label}</span>
            <p>{value}</p>
        </div>
    );
}

export default App;
