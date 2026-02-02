import { useState, useEffect } from 'react';
import axios from 'axios';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';
import './App.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

// Configure Axios
const api = axios.create({
    baseURL: '/api'
});

function App() {
    const [user, setUser] = useState(null);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const [uploadId, setUploadId] = useState(null);
    const [summary, setSummary] = useState(null);
    const [history, setHistory] = useState([]);
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    // Check for existing session/basic auth on mount (optional - not fully persisting for basic auth demo)
    // For Basic Auth we usually send headers with every request.
    // For this simple demo, we'll store credentials in state (or base64 encoded token).
    const [authHeader, setAuthHeader] = useState(null);

    useEffect(() => {
        if (authHeader) {
            fetchHistory();
        }
    }, [authHeader]);

    useEffect(() => {
        if (uploadId && authHeader) {
            fetchSummary(uploadId);
        }
    }, [uploadId, authHeader]);

    const handleLogin = (e) => {
        e.preventDefault();
        // In a real app we'd get a token. Here we just set the Basic Auth header.
        // We'll verify it by making a simple call.
        const token = 'Basic ' + btoa(username + ':' + password);
        api.defaults.headers.common['Authorization'] = token;

        api.get('/uploads/history/')
            .then(res => {
                setAuthHeader(token);
                setUser(username);
                setHistory(res.data);
            })
            .catch(err => {
                alert('Invalid Credentials');
            });
    };

    const handleLogout = () => {
        setAuthHeader(null);
        setUser(null);
        setUploadId(null);
        setSummary(null);
        setHistory([]);
        delete api.defaults.headers.common['Authorization'];
    };

    const fetchHistory = async () => {
        try {
            const res = await api.get('/uploads/history/');
            setHistory(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const fetchSummary = async (id) => {
        try {
            const res = await api.get(`/uploads/${id}/summary/`);
            setSummary(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await api.post('/uploads/', formData);
            setUploadId(res.data.id);
            fetchHistory();
            alert('Upload Successful!');
        } catch (err) {
            alert('Upload Failed');
        } finally {
            setLoading(false);
        }
    };

    const handleDownloadPDF = async () => {
        if (!uploadId) return;
        try {
            const response = await api.get(`/uploads/${uploadId}/generate_pdf/`, {
                responseType: 'blob', // Important
            });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `report_upload_${uploadId}.pdf`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (err) {
            console.error(err);
            alert("Failed to download PDF");
        }
    };

    const chartData = summary ? {
        labels: summary.type_distribution.map(d => d.equipment_type),
        datasets: [
            {
                label: 'Equipment Count',
                data: summary.type_distribution.map(d => d.count),
                backgroundColor: 'rgba(56, 189, 248, 0.6)',
                borderColor: 'rgba(56, 189, 248, 1)',
                borderWidth: 1,
                borderRadius: 4,
            },
        ],
    } : null;

    const chartOptions = {
        responsive: true,
        plugins: {
            legend: {
                labels: { color: '#94a3b8' }
            },
            title: {
                display: false,
            }
        },
        scales: {
            y: {
                grid: { color: '#334155' },
                ticks: { color: '#94a3b8' }
            },
            x: {
                grid: { display: false },
                ticks: { color: '#94a3b8' }
            }
        }
    };

    if (!user) {
        return (
            <div className="login-container">
                <div className="login-box">
                    <h1>Visualizer Login</h1>
                    <form onSubmit={handleLogin}>
                        <div className="form-group">
                            <label>Username</label>
                            <input
                                type="text"
                                className="form-input"
                                value={username}
                                onChange={e => setUsername(e.target.value)}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Password</label>
                            <input
                                type="password"
                                className="form-input"
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                required
                            />
                        </div>
                        <button type="submit" className="btn-primary btn-full">Sign In</button>
                    </form>
                </div>
            </div>
        );
    }

    return (
        <div className="container">
            <nav className="navbar">
                <h1>Chemical Equipment Visualizer</h1>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <span style={{ color: '#94a3b8' }}>Welcome, {user}</span>
                    <button onClick={handleLogout} className="logout-btn">Logout</button>
                </div>
            </nav>

            <div className="main-content">
                <aside className="sidebar">
                    <h3>Recent Uploads</h3>
                    <ul>
                        {history.map(h => (
                            <li key={h.id} onClick={() => setUploadId(h.id)} className={uploadId === h.id ? 'active' : ''}>
                                <strong>Upload #{h.id}</strong> <br /> <small>{new Date(h.uploaded_at).toLocaleDateString()} {new Date(h.uploaded_at).toLocaleTimeString()}</small>
                            </li>
                        ))}
                    </ul>
                </aside>

                <section className="workspace">
                    <div className="upload-section">
                        <div className="file-input-wrapper">
                            <input className="file-input" type="file" onChange={(e) => setFile(e.target.files[0])} accept=".csv" />
                        </div>
                        <button onClick={handleUpload} className="btn-primary" disabled={loading}>
                            {loading ? 'Uploading...' : 'Upload New CSV'}
                        </button>

                        {summary && (
                            <button onClick={handleDownloadPDF} className="btn-secondary">
                                Download PDF Report
                            </button>
                        )}
                    </div>

                    {summary ? (
                        <div className="dashboard">
                            <div className="scorecards">
                                <div className="card">
                                    <h3>Total Equipment</h3>
                                    <p>{summary.total_count}</p>
                                </div>
                                <div className="card">
                                    <h3>Avg Flowrate</h3>
                                    <p>{summary.averages.flowrate}</p>
                                </div>
                                <div className="card">
                                    <h3>Avg Pressure</h3>
                                    <p>{summary.averages.pressure}</p>
                                </div>
                                <div className="card">
                                    <h3>Avg Temp (C)</h3>
                                    <p>{summary.averages.temperature}</p>
                                </div>
                            </div>

                            <div className="chart-container">
                                <h3 style={{ marginBottom: '1rem', color: '#94a3b8' }}>Equipment Type Distribution</h3>
                                {chartData && <Bar data={chartData} options={chartOptions} />}
                            </div>
                        </div>
                    ) : (
                        <div className="placeholder">
                            <h2>Select a dataset from history or upload a new file to view analytics.</h2>
                            <p style={{ marginTop: '1rem', fontSize: '0.9rem' }}>Supported format: CSV with Equipment Name, Type, Flowrate, etc.</p>
                        </div>
                    )}
                </section>
            </div>
        </div>
    );
}

export default App;
