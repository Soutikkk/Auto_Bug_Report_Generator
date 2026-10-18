/**
 * AutoBug.io - Application Logic & Real-time Diagnostic Studio
 * =============================================================
 * Handles dashboard metrics, report parsing, live bug simulations,
 * heuristic remediation insights, and export pipelines.
 */

// Initial mock reports for offline/static preview
const INITIAL_MOCK_REPORTS = [
    {
        filename: "bug_report_ZeroDivisionError_20261016_103217.txt",
        error_type: "ZeroDivisionError",
        error_message: "division by zero",
        date_time: "2026-10-16 10:32:17",
        file_name: "C:\\Users\\USER\\Desktop\\MISCELLANEOUS\\Mini Projects\\Auto Bug Report Generator\\sample_code.py",
        line_number: "27",
        function_name: "calculate_average()",
        code_line: "average = total_score / number_of_students",
        traceback: `Traceback (most recent call last):
  File "bug_reporter.py", line 272, in wrapper
    return func(*args, **kwargs)
  File "sample_code.py", line 27, in calculate_average
    average = total_score / number_of_students
ZeroDivisionError: division by zero`,
        python_version: "3.12.4",
        os_platform: "win32",
        raw_text: `==============================================================================
                        AUTO BUG REPORT GENERATOR
==============================================================================
1. Date & Time       : 2026-10-16 10:32:17
2. Error Type        : ZeroDivisionError
3. Error Message     : division by zero
4. File Name         : C:\\Users\\USER\\Desktop\\MISCELLANEOUS\\Mini Projects\\Auto Bug Report Generator\\sample_code.py
5. Line Number       : 27
6. Function / Scope  : calculate_average()
7. Failing Code Line : average = total_score / number_of_students
==============================================================================
SHORT TRACEBACK:
==============================================================================
Traceback (most recent call last):
  File "bug_reporter.py", line 272, in wrapper
    return func(*args, **kwargs)
  File "sample_code.py", line 27, in calculate_average
    average = total_score / number_of_students
ZeroDivisionError: division by zero
==============================================================================
SYSTEM CONTEXT:
==============================================================================
Python Version       : 3.12.4
Operating System     : win32
Execution Directory  : C:\\Users\\USER\\Desktop\\MISCELLANEOUS\\Mini Projects\\Auto Bug Report Generator
==============================================================================
                     END OF REPORT
==============================================================================`
    },
    {
        filename: "bug_report_KeyError_20261016_103217.txt",
        error_type: "KeyError",
        error_message: "'account_id'",
        date_time: "2026-10-16 10:32:17",
        file_name: "C:\\Users\\USER\\Desktop\\MISCELLANEOUS\\Mini Projects\\Auto Bug Report Generator\\sample_code.py",
        line_number: "64",
        function_name: "parse_user_profile()",
        code_line: "account_id = user_data['account_id']",
        traceback: `Traceback (most recent call last):
  File "sample_code.py", line 83, in run_all_samples
    parse_user_profile()
  File "sample_code.py", line 64, in parse_user_profile
    account_id = user_data['account_id']
KeyError: 'account_id'`,
        python_version: "3.12.4",
        os_platform: "win32",
        raw_text: `==============================================================================
                        AUTO BUG REPORT GENERATOR
==============================================================================
1. Date & Time       : 2026-10-16 10:32:17
2. Error Type        : KeyError
3. Error Message     : 'account_id'
4. File Name         : C:\\Users\\USER\\Desktop\\MISCELLANEOUS\\Mini Projects\\Auto Bug Report Generator\\sample_code.py
5. Line Number       : 64
6. Function / Scope  : parse_user_profile()
7. Failing Code Line : account_id = user_data['account_id']
==============================================================================
SHORT TRACEBACK:
==============================================================================
Traceback (most recent call last):
  File "sample_code.py", line 83, in run_all_samples
    parse_user_profile()
  File "sample_code.py", line 64, in parse_user_profile
    account_id = user_data['account_id']
KeyError: 'account_id'
==============================================================================
SYSTEM CONTEXT:
==============================================================================
Python Version       : 3.12.4
Operating System     : win32
Execution Directory  : C:\\Users\\USER\\Desktop\\MISCELLANEOUS\\Mini Projects\\Auto Bug Report Generator
==============================================================================
                     END OF REPORT
==============================================================================`
    },
    {
        filename: "bug_report_FileNotFoundError_20261016_103217.txt",
        error_type: "FileNotFoundError",
        error_message: "[Errno 2] No such file or directory: 'non_existent_database.ini'",
        date_time: "2026-10-16 10:32:17",
        file_name: "C:\\Users\\USER\\Desktop\\MISCELLANEOUS\\Mini Projects\\Auto Bug Report Generator\\sample_code.py",
        line_number: "43",
        function_name: "load_configuration_file()",
        code_line: "with open(file_name, 'r') as f:",
        traceback: `Traceback (most recent call last):
  File "sample_code.py", line 43, in load_configuration_file
    with open(file_name, 'r') as f:
FileNotFoundError: [Errno 2] No such file or directory: 'non_existent_database.ini'`,
        python_version: "3.12.4",
        os_platform: "win32",
        raw_text: `==============================================================================
                        AUTO BUG REPORT GENERATOR
==============================================================================
1. Date & Time       : 2026-10-16 10:32:17
2. Error Type        : FileNotFoundError
3. Error Message     : [Errno 2] No such file or directory: 'non_existent_database.ini'
4. File Name         : C:\\Users\\USER\\Desktop\\MISCELLANEOUS\\Mini Projects\\Auto Bug Report Generator\\sample_code.py
5. Line Number       : 43
6. Function / Scope  : load_configuration_file()
7. Failing Code Line : with open(file_name, 'r') as f:
==============================================================================
SHORT TRACEBACK:
==============================================================================
Traceback (most recent call last):
  File "sample_code.py", line 43, in load_configuration_file
    with open(file_name, 'r') as f:
FileNotFoundError: [Errno 2] No such file or directory: 'non_existent_database.ini'
==============================================================================
SYSTEM CONTEXT:
==============================================================================
Python Version       : 3.12.4
Operating System     : win32
Execution Directory  : C:\\Users\\USER\\Desktop\\MISCELLANEOUS\\Mini Projects\\Auto Bug Report Generator
==============================================================================
                     END OF REPORT
==============================================================================`
    }
];

// Presets for Studio Generator
const STUDIO_PRESETS = {
    zero_div: {
        type: "ZeroDivisionError",
        message: "division by zero",
        file: "analytics_engine.py",
        line: "108",
        code: "conversion_rate = completed_orders / total_visitors",
        traceback: `Traceback (most recent call last):
  File "analytics_engine.py", line 108, in compute_kpis
    conversion_rate = completed_orders / total_visitors
ZeroDivisionError: division by zero`
    },
    key_error: {
        type: "KeyError",
        message: "'auth_token'",
        file: "auth_service.py",
        line: "54",
        code: "token = session_payload['auth_token']",
        traceback: `Traceback (most recent call last):
  File "auth_service.py", line 54, in verify_request
    token = session_payload['auth_token']
KeyError: 'auth_token'`
    },
    file_not_found: {
        type: "FileNotFoundError",
        message: "[Errno 2] No such file or directory: 'secrets/prod.env'",
        file: "config_loader.py",
        line: "32",
        code: "with open('secrets/prod.env', 'r') as env_file:",
        traceback: `Traceback (most recent call last):
  File "config_loader.py", line 32, in load_env
    with open('secrets/prod.env', 'r') as env_file:
FileNotFoundError: [Errno 2] No such file or directory: 'secrets/prod.env'`
    },
    index_error: {
        type: "IndexError",
        message: "list index out of range",
        file: "parser_pipeline.py",
        line: "77",
        code: "primary_id = tokens[0]",
        traceback: `Traceback (most recent call last):
  File "parser_pipeline.py", line 77, in parse_tokens
    primary_id = tokens[0]
IndexError: list index out of range`
    },
    type_error: {
        type: "TypeError",
        message: "unsupported operand type(s) for +: 'int' and 'str'",
        file: "payment_processor.py",
        line: "91",
        code: "total_amount = base_price + tax_string",
        traceback: `Traceback (most recent call last):
  File "payment_processor.py", line 91, in compute_charge
    total_amount = base_price + tax_string
TypeError: unsupported operand type(s) for +: 'int' and 'str'`
    },
    custom: {
        type: "",
        message: "",
        file: "",
        line: "",
        code: "",
        traceback: ""
    }
};

// Remediation Knowledge Base
const REMEDIATION_KNOWLEDGE = {
    ZeroDivisionError: {
        title: "Zero Division Guard Suggestion",
        advice: "Guard against 0 denominators with a safe ternary or conditional check. E.g.: `result = numerator / denominator if denominator != 0 else 0.0` or provide an explicit default."
    },
    KeyError: {
        title: "Dictionary Key Access Remediation",
        advice: "Avoid direct bracket indexing `dict[key]` for optional fields. Instead, use safe retrieval: `dict.get('key', default_value)` or test presence with `if 'key' in dict:`."
    },
    FileNotFoundError: {
        title: "File Path & Working Directory Hint",
        advice: "Verify that the target path exists using `pathlib.Path(filename).exists()` and ensure relative paths are anchored with `Path(__file__).parent / filename`."
    },
    IndexError: {
        title: "Bounds Checking Suggestion",
        advice: "Ensure the list contains elements prior to indexing: `if items: first = items[0]` or wrap in a slicing notation `items[:1]` which returns an empty list instead of throwing."
    },
    TypeError: {
        title: "Type Coercion & Validation Recommendation",
        advice: "Enforce type checks or explicit casts before operations: e.g. `float(tax_string)` or check with `isinstance(obj, (int, float))`."
    },
    Default: {
        title: "General Defensive Programming Insight",
        advice: "Inspect stack frame variables and enclose fragile operations in a `with MonitorErrors(reports_dir='reports')` context to capture diagnostics without crashing your runtime."
    }
};

// State Store
let state = {
    reports: [...INITIAL_MOCK_REPORTS],
    activeFilter: 'all',
    searchQuery: '',
    selectedReportFilename: null,
    isServerConnected: false
};

// DOM Elements
const elements = {
    navTabs: document.querySelectorAll('.nav-item'),
    tabContents: document.querySelectorAll('.tab-content'),
    pageHeading: document.getElementById('page-heading'),
    reportCountBadge: document.getElementById('report-count-badge'),
    serverStatusDot: document.getElementById('server-status-dot'),
    serverStatusText: document.getElementById('server-status-text'),
    serverStatusDetail: document.getElementById('server-status-detail'),
    
    // Stats
    statTotalCrashes: document.getElementById('stat-total-crashes'),
    statTopException: document.getElementById('stat-top-exception'),
    statTopExceptionCount: document.getElementById('stat-top-exception-count'),
    recentReportsContainer: document.getElementById('recent-reports-container'),
    errorBreakdownContainer: document.getElementById('error-breakdown-container'),

    // Explorer
    searchInput: document.getElementById('report-search-input'),
    filterPills: document.querySelectorAll('.filter-pill'),
    reportsListContainer: document.getElementById('reports-list-container'),
    reportDetailContainer: document.getElementById('report-detail-container'),

    // Studio
    presetSelector: document.getElementById('preset-selector'),
    inputErrorType: document.getElementById('input-error-type'),
    inputErrorMessage: document.getElementById('input-error-message'),
    inputFileName: document.getElementById('input-file-name'),
    inputLineNumber: document.getElementById('input-line-number'),
    inputCodeLine: document.getElementById('input-code-line'),
    inputTraceback: document.getElementById('input-traceback'),
    btnGenerateCustomReport: document.getElementById('btn-generate-custom-report'),
    studioOutputPreview: document.getElementById('studio-output-preview'),
    studioRemediationText: document.getElementById('studio-remediation-text'),
    btnCopyStudioText: document.getElementById('btn-copy-studio-text'),
    btnDownloadStudioTxt: document.getElementById('btn-download-studio-txt'),

    // Global Buttons
    btnRefreshReports: document.getElementById('btn-refresh-reports'),
    btnQuickSimulate: document.getElementById('btn-quick-simulate'),
    linkViewAllReports: document.getElementById('link-view-all-reports'),
    toastContainer: document.getElementById('toast-container')
};

// ==========================================================================
// Initialization
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
    setupNavigation();
    setupFiltersAndSearch();
    setupStudioPresets();
    setupSimulationButtons();
    loadReportsFromServer();
});

// --------------------------------------------------------------------------
// Navigation & Tab Switching
// --------------------------------------------------------------------------
function setupNavigation() {
    elements.navTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetId = tab.getAttribute('data-tab');
            switchTab(targetId);
        });
    });

    if (elements.linkViewAllReports) {
        elements.linkViewAllReports.addEventListener('click', () => {
            switchTab('explorer-tab');
        });
    }

    if (elements.btnQuickSimulate) {
        elements.btnQuickSimulate.addEventListener('click', () => {
            simulateError('zero_division');
        });
    }

    if (elements.btnRefreshReports) {
        elements.btnRefreshReports.addEventListener('click', () => {
            loadReportsFromServer(true);
        });
    }
}

function switchTab(tabId) {
    elements.navTabs.forEach(tab => {
        if (tab.getAttribute('data-tab') === tabId) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });

    elements.tabContents.forEach(content => {
        if (content.id === tabId) {
            content.classList.add('active');
        } else {
            content.classList.remove('active');
        }
    });

    // Update Topbar Title
    const titles = {
        'dashboard-tab': 'Diagnostics & Monitoring Dashboard',
        'explorer-tab': 'Report Explorer & Trace Inspector',
        'studio-tab': 'Diagnostic Studio & Synthesizer',
        'docs-tab': 'Integration & Architecture Guide'
    };
    if (elements.pageHeading && titles[tabId]) {
        elements.pageHeading.textContent = titles[tabId];
    }
}

// --------------------------------------------------------------------------
// Server Sync & Report Loading
// --------------------------------------------------------------------------
async function loadReportsFromServer(showToastNotice = false) {
    try {
        const response = await fetch('/api/reports', { cache: 'no-store' });
        if (response.ok) {
            const data = await response.json();
            if (Array.isArray(data) && data.length > 0) {
                state.reports = data;
            }
            setServerConnected(true);
            if (showToastNotice) {
                showToast(`Refreshed ${state.reports.length} bug reports from disk`, 'success');
            }
        } else {
            setServerConnected(false);
        }
    } catch (err) {
        // Standalone browser mode without python web_server running
        setServerConnected(false);
        if (showToastNotice) {
            showToast('Loaded in offline standalone preview mode', 'info');
        }
    }

    renderAllViews();
}

function setServerConnected(connected) {
    state.isServerConnected = connected;
    if (connected) {
        elements.serverStatusDot.style.background = 'var(--color-emerald)';
        elements.serverStatusDot.style.boxShadow = '0 0 10px var(--color-emerald)';
        elements.serverStatusText.textContent = 'Server Live';
        elements.serverStatusText.style.color = 'var(--color-emerald)';
        elements.serverStatusDetail.textContent = 'REST API Connected';
    } else {
        elements.serverStatusDot.style.background = 'var(--color-cyan)';
        elements.serverStatusDot.style.boxShadow = '0 0 10px var(--color-cyan)';
        elements.serverStatusText.textContent = 'Standalone Mode';
        elements.serverStatusText.style.color = 'var(--color-cyan)';
        elements.serverStatusDetail.textContent = 'Client-Side Synthesizer';
    }
}

// --------------------------------------------------------------------------
// Render Functions
// --------------------------------------------------------------------------
function renderAllViews() {
    renderDashboardMetrics();
    renderRecentReports();
    renderErrorBreakdown();
    renderExplorerList();
    updateBadges();

    // Auto-select first report if none selected
    if (!state.selectedReportFilename && state.reports.length > 0) {
        selectReport(state.reports[0].filename);
    }
}

function updateBadges() {
    if (elements.reportCountBadge) {
        elements.reportCountBadge.textContent = state.reports.length;
    }
}

function renderDashboardMetrics() {
    const total = state.reports.length;
    elements.statTotalCrashes.textContent = total;

    // Calculate top exception
    const counts = {};
    state.reports.forEach(r => {
        counts[r.error_type] = (counts[r.error_type] || 0) + 1;
    });

    let topType = 'None';
    let topCount = 0;
    for (const [type, count] of Object.entries(counts)) {
        if (count > topCount) {
            topType = type;
            topCount = count;
        }
    }

    elements.statTopException.textContent = topType;
    elements.statTopExceptionCount.textContent = `${topCount} occurrence${topCount === 1 ? '' : 's'}`;
}

function renderRecentReports() {
    if (!elements.recentReportsContainer) return;
    elements.recentReportsContainer.innerHTML = '';

    const recents = state.reports.slice(0, 5);
    if (recents.length === 0) {
        elements.recentReportsContainer.innerHTML = `
            <div class="empty-state">
                <p>No crash reports recorded yet.</p>
            </div>
        `;
        return;
    }

    recents.forEach(report => {
        const item = document.createElement('div');
        item.className = 'report-summary-item';
        item.innerHTML = `
            <div class="report-summary-main">
                <span class="error-tag ${getTagClass(report.error_type)}">${escapeHtml(report.error_type)}</span>
                <div class="report-summary-details">
                    <span class="report-summary-title">${escapeHtml(report.error_message)}</span>
                    <span class="report-summary-meta">${escapeHtml(getBasename(report.file_name))}:${report.line_number} in <code>${escapeHtml(report.function_name)}</code></span>
                </div>
            </div>
            <span class="report-summary-time">${escapeHtml(report.date_time)}</span>
        `;
        item.addEventListener('click', () => {
            selectReport(report.filename);
            switchTab('explorer-tab');
        });
        elements.recentReportsContainer.appendChild(item);
    });
}

function renderErrorBreakdown() {
    if (!elements.errorBreakdownContainer) return;
    elements.errorBreakdownContainer.innerHTML = '';

    const counts = {};
    const total = state.reports.length || 1;
    state.reports.forEach(r => {
        counts[r.error_type] = (counts[r.error_type] || 0) + 1;
    });

    const colors = {
        ZeroDivisionError: 'var(--color-rose)',
        KeyError: 'var(--color-amber)',
        FileNotFoundError: 'var(--color-cyan)',
        IndexError: 'var(--color-purple)',
        TypeError: '#38bdf8'
    };

    for (const [type, count] of Object.entries(counts)) {
        const pct = Math.round((count / total) * 100);
        const color = colors[type] || 'var(--accent-primary)';
        const row = document.createElement('div');
        row.className = 'breakdown-row';
        row.innerHTML = `
            <div class="breakdown-label-row">
                <span class="breakdown-label">${escapeHtml(type)}</span>
                <span class="breakdown-pct">${count} (${pct}%)</span>
            </div>
            <div class="breakdown-bar-bg">
                <div class="breakdown-bar-fill" style="width: ${pct}%; background: ${color};"></div>
            </div>
        `;
        elements.errorBreakdownContainer.appendChild(row);
    }
}

// --------------------------------------------------------------------------
// Report Explorer
// --------------------------------------------------------------------------
function setupFiltersAndSearch() {
    if (elements.searchInput) {
        elements.searchInput.addEventListener('input', (e) => {
            state.searchQuery = e.target.value.toLowerCase().trim();
            renderExplorerList();
        });
    }

    elements.filterPills.forEach(pill => {
        pill.addEventListener('click', () => {
            elements.filterPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            state.activeFilter = pill.getAttribute('data-filter');
            renderExplorerList();
        });
    });
}

function renderExplorerList() {
    if (!elements.reportsListContainer) return;
    elements.reportsListContainer.innerHTML = '';

    const filtered = state.reports.filter(report => {
        const matchesFilter = (state.activeFilter === 'all') ||
            (state.activeFilter === 'Other' ? !['ZeroDivisionError', 'KeyError', 'FileNotFoundError'].includes(report.error_type) : report.error_type === state.activeFilter);

        const matchesSearch = !state.searchQuery ||
            report.error_type.toLowerCase().includes(state.searchQuery) ||
            report.error_message.toLowerCase().includes(state.searchQuery) ||
            report.file_name.toLowerCase().includes(state.searchQuery) ||
            report.date_time.toLowerCase().includes(state.searchQuery);

        return matchesFilter && matchesSearch;
    });

    if (filtered.length === 0) {
        elements.reportsListContainer.innerHTML = `
            <div style="text-align: center; color: var(--text-dim); padding: 30px;">
                <p>No matching reports found.</p>
            </div>
        `;
        return;
    }

    filtered.forEach(report => {
        const card = document.createElement('div');
        card.className = `report-item-card ${state.selectedReportFilename === report.filename ? 'selected' : ''}`;
        card.innerHTML = `
            <div class="report-card-top">
                <span class="error-tag ${getTagClass(report.error_type)}">${escapeHtml(report.error_type)}</span>
                <span class="report-summary-time">${escapeHtml(report.date_time.split(' ')[1] || report.date_time)}</span>
            </div>
            <div class="report-card-filename">${escapeHtml(getBasename(report.file_name))}</div>
            <div class="report-card-failing-line">${escapeHtml(report.error_message)}</div>
        `;
        card.addEventListener('click', () => {
            selectReport(report.filename);
        });
        elements.reportsListContainer.appendChild(card);
    });
}

function selectReport(filename) {
    state.selectedReportFilename = filename;
    renderExplorerList();

    const report = state.reports.find(r => r.filename === filename);
    if (!report || !elements.reportDetailContainer) return;

    const guidance = REMEDIATION_KNOWLEDGE[report.error_type] || REMEDIATION_KNOWLEDGE.Default;

    elements.reportDetailContainer.innerHTML = `
        <div class="report-detail-view">
            <div class="detail-header">
                <div class="detail-title-group">
                    <h2>
                        <span class="error-tag ${getTagClass(report.error_type)}">${escapeHtml(report.error_type)}</span>
                        ${escapeHtml(report.error_message)}
                    </h2>
                    <div class="detail-file-meta">
                        <span>Report File: <strong>${escapeHtml(report.filename)}</strong></span>
                    </div>
                </div>
                <div class="detail-actions">
                    <button class="btn btn-secondary btn-copy-txt" title="Copy raw text format">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                        </svg>
                        <span>Copy TXT</span>
                    </button>
                    <button class="btn btn-secondary btn-copy-md" title="Copy formatted Markdown for GitHub issue">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="16 18 22 12 16 6"/>
                            <polyline points="8 6 2 12 8 18"/>
                        </svg>
                        <span>Markdown</span>
                    </button>
                    <button class="btn btn-primary btn-download" title="Save .txt report to disk">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                            <polyline points="7 10 12 15 17 10"/>
                            <line x1="12" y1="15" x2="12" y2="3"/>
                        </svg>
                        <span>Export</span>
                    </button>
                </div>
            </div>

            <!-- Key Context Metadata -->
            <div class="detail-meta-grid">
                <div class="meta-box">
                    <span class="meta-box-label">Timestamp</span>
                    <div class="meta-box-val">${escapeHtml(report.date_time)}</div>
                </div>
                <div class="meta-box">
                    <span class="meta-box-label">Source Location</span>
                    <div class="meta-box-val">${escapeHtml(getBasename(report.file_name))}:${report.line_number}</div>
                </div>
                <div class="meta-box">
                    <span class="meta-box-label">Function Scope</span>
                    <div class="meta-box-val">${escapeHtml(report.function_name)}</div>
                </div>
            </div>

            <!-- AI Remediation Box -->
            <div class="remediation-box">
                <div class="remediation-title">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                    </svg>
                    <span>${escapeHtml(guidance.title)}</span>
                </div>
                <p class="remediation-content">${escapeHtml(guidance.advice)}</p>
            </div>

            <!-- Failing Code Line -->
            <div>
                <h4 class="section-heading">Failing Code Statement</h4>
                <div class="failing-code-line">
                    ${escapeHtml(report.code_line || 'N/A')}
                </div>
            </div>

            <!-- Traceback Section -->
            <div>
                <h4 class="section-heading">Short Formatted Traceback</h4>
                <pre class="code-box"><code>${escapeHtml(report.traceback || 'No traceback captured.')}</code></pre>
            </div>

            <!-- System Context -->
            <div class="detail-meta-grid">
                <div class="meta-box">
                    <span class="meta-box-label">Python Version</span>
                    <div class="meta-box-val">${escapeHtml(report.python_version || '3.12')}</div>
                </div>
                <div class="meta-box">
                    <span class="meta-box-label">Operating System</span>
                    <div class="meta-box-val">${escapeHtml(report.os_platform || 'win32')}</div>
                </div>
                <div class="meta-box">
                    <span class="meta-box-label">Absolute Path</span>
                    <div class="meta-box-val" style="font-size: 0.75rem;">${escapeHtml(report.file_name)}</div>
                </div>
            </div>
        </div>
    `;

    // Bind action buttons
    const btnCopyTxt = elements.reportDetailContainer.querySelector('.btn-copy-txt');
    const btnCopyMd = elements.reportDetailContainer.querySelector('.btn-copy-md');
    const btnDownload = elements.reportDetailContainer.querySelector('.btn-download');

    if (btnCopyTxt) {
        btnCopyTxt.addEventListener('click', () => {
            navigator.clipboard.writeText(report.raw_text || generateRawReportText(report));
            showToast('Copied raw report to clipboard', 'success');
        });
    }

    if (btnCopyMd) {
        btnCopyMd.addEventListener('click', () => {
            const md = generateMarkdownReport(report);
            navigator.clipboard.writeText(md);
            showToast('Copied GitHub-flavored Markdown', 'success');
        });
    }

    if (btnDownload) {
        btnDownload.addEventListener('click', () => {
            downloadFile(report.filename, report.raw_text || generateRawReportText(report));
            showToast(`Downloaded ${report.filename}`, 'success');
        });
    }
}

// --------------------------------------------------------------------------
// Bug Studio & Generator
// --------------------------------------------------------------------------
function setupStudioPresets() {
    if (!elements.presetSelector) return;

    elements.presetSelector.addEventListener('change', (e) => {
        const val = e.target.value;
        const preset = STUDIO_PRESETS[val];
        if (preset) {
            elements.inputErrorType.value = preset.type;
            elements.inputErrorMessage.value = preset.message;
            elements.inputFileName.value = preset.file;
            elements.inputLineNumber.value = preset.line;
            elements.inputCodeLine.value = preset.code;
            elements.inputTraceback.value = preset.traceback;
        }
    });

    // Load initial preset
    elements.presetSelector.value = 'zero_div';
    elements.presetSelector.dispatchEvent(new Event('change'));

    // Bind generator button
    if (elements.btnGenerateCustomReport) {
        elements.btnGenerateCustomReport.addEventListener('click', handleStudioGenerate);
    }

    // Bind studio copy & download
    if (elements.btnCopyStudioText) {
        elements.btnCopyStudioText.addEventListener('click', () => {
            const text = elements.studioOutputPreview.textContent;
            navigator.clipboard.writeText(text);
            showToast('Copied studio output', 'success');
        });
    }

    if (elements.btnDownloadStudioTxt) {
        elements.btnDownloadStudioTxt.addEventListener('click', () => {
            const type = elements.inputErrorType.value.trim() || 'CustomError';
            const timestamp = formatIsoDateFile(new Date());
            const filename = `bug_report_${type}_${timestamp}.txt`;
            downloadFile(filename, elements.studioOutputPreview.textContent);
            showToast(`Exported ${filename}`, 'success');
        });
    }
}

async function handleStudioGenerate() {
    const errorType = elements.inputErrorType.value.trim() || 'RuntimeError';
    const errorMessage = elements.inputErrorMessage.value.trim() || 'Unexpected execution failure';
    const fileName = elements.inputFileName.value.trim() || 'app.py';
    const lineNumber = elements.inputLineNumber.value.trim() || '1';
    const codeLine = elements.inputCodeLine.value.trim() || '# Failing line not specified';
    const traceback = elements.inputTraceback.value.trim() || `Traceback (most recent call last):\n  File "${fileName}", line ${lineNumber}\n${errorType}: ${errorMessage}`;

    const now = new Date();
    const dateFormatted = formatStandardDate(now);
    const fileTimestamp = formatIsoDateFile(now);
    const filename = `bug_report_${errorType}_${fileTimestamp}.txt`;

    const reportObj = {
        filename,
        error_type: errorType,
        error_message: errorMessage,
        date_time: dateFormatted,
        file_name: fileName,
        line_number: lineNumber,
        function_name: '<module>',
        code_line: codeLine,
        traceback: traceback,
        python_version: '3.12.4',
        os_platform: 'win32'
    };

    reportObj.raw_text = generateRawReportText(reportObj);

    // If server is available, attempt to post to backend
    if (state.isServerConnected) {
        try {
            await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(reportObj)
            });
        } catch (err) {
            console.warn('Backend save failed, keeping in memory', err);
        }
    }

    // Update studio preview
    elements.studioOutputPreview.textContent = reportObj.raw_text;

    // Update remediation text
    const guidance = REMEDIATION_KNOWLEDGE[errorType] || REMEDIATION_KNOWLEDGE.Default;
    elements.studioRemediationText.textContent = `${guidance.title}: ${guidance.advice}`;

    // Add to state and refresh views
    state.reports.unshift(reportObj);
    renderAllViews();
    showToast(`Generated: ${filename}`, 'success');
}

// --------------------------------------------------------------------------
// Simulation Triggers
// --------------------------------------------------------------------------
function setupSimulationButtons() {
    const simButtons = document.querySelectorAll('[data-simulate]');
    simButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const scenario = btn.getAttribute('data-simulate');
            simulateError(scenario);
        });
    });
}

async function simulateError(scenario) {
    showToast(`Simulating ${scenario.replace('_', ' ')}...`, 'info');

    if (state.isServerConnected) {
        try {
            const res = await fetch('/api/simulate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ scenario })
            });
            if (res.ok) {
                const newReport = await res.json();
                state.reports.unshift(newReport);
                renderAllViews();
                selectReport(newReport.filename);
                showToast(`Caught & generated: ${newReport.error_type}`, 'success');
                return;
            }
        } catch (err) {
            console.warn('Simulation server call failed, using client simulation', err);
        }
    }

    // Client-side simulation fallback
    const presetKey = scenario === 'zero_division' ? 'zero_div' : scenario === 'missing_key' ? 'key_error' : 'file_not_found';
    const p = STUDIO_PRESETS[presetKey];
    const now = new Date();
    const dateFormatted = formatStandardDate(now);
    const fileTimestamp = formatIsoDateFile(now);
    const filename = `bug_report_${p.type}_${fileTimestamp}.txt`;

    const simReport = {
        filename,
        error_type: p.type,
        error_message: p.message,
        date_time: dateFormatted,
        file_name: p.file,
        line_number: p.line,
        function_name: 'simulated_pipeline()',
        code_line: p.code,
        traceback: p.traceback,
        python_version: '3.12.4',
        os_platform: 'win32'
    };
    simReport.raw_text = generateRawReportText(simReport);

    state.reports.unshift(simReport);
    renderAllViews();
    selectReport(simReport.filename);
    showToast(`Simulated & generated: ${simReport.error_type}`, 'success');
}

// --------------------------------------------------------------------------
// Helper Generators & Formatters
// --------------------------------------------------------------------------
function generateRawReportText(r) {
    return `==============================================================================
                        AUTO BUG REPORT GENERATOR
==============================================================================
1. Date & Time       : ${r.date_time}
2. Error Type        : ${r.error_type}
3. Error Message     : ${r.error_message}
4. File Name         : ${r.file_name}
5. Line Number       : ${r.line_number}
6. Function / Scope  : ${r.function_name || '<module>'}
7. Failing Code Line : ${r.code_line || 'N/A'}
==============================================================================
SHORT TRACEBACK:
==============================================================================
${r.traceback || 'No traceback captured.'}
==============================================================================
SYSTEM CONTEXT:
==============================================================================
Python Version       : ${r.python_version || '3.12.4'}
Operating System     : ${r.os_platform || 'win32'}
Execution Directory  : C:\\AutoBugReportGenerator
==============================================================================
                     END OF REPORT
==============================================================================`;
}

function generateMarkdownReport(r) {
    return `## 🚨 Auto Bug Report: \`${r.error_type}\`

**Error Message:** \`${r.error_message}\`  
**Timestamp:** ${r.date_time}  
**Source Location:** \`${getBasename(r.file_name)}:${r.line_number}\` in \`${r.function_name || 'root'}\`

### 💥 Failing Code
\`\`\`python
${r.code_line || '# Not captured'}
\`\`\`

### 📜 Traceback
\`\`\`text
${r.traceback}
\`\`\`

---
*Generated automatically by Auto Bug Report Generator*`;
}

function getTagClass(errorType) {
    if (errorType === 'ZeroDivisionError') return 'tag-ZeroDivisionError';
    if (errorType === 'KeyError') return 'tag-KeyError';
    if (errorType === 'FileNotFoundError') return 'tag-FileNotFoundError';
    return 'tag-custom';
}

function getBasename(filePath) {
    if (!filePath) return 'unknown';
    const parts = filePath.split(/[/\\]/);
    return parts[parts.length - 1];
}

function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function formatStandardDate(d) {
    const pad = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}

function formatIsoDateFile(d) {
    const pad = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}_${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
}

function downloadFile(filename, content) {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function showToast(message, type = 'info') {
    if (!elements.toastContainer) return;
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    elements.toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3200);
}
