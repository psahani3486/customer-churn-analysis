/**
 * ChurnScope — Main Application Controller
 * Initializes dashboard, loads data from API, and handles user interactions.
 */

document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

async function initApp() {
    const overlay = document.getElementById('loading-overlay');

    try {
        // Check API health
        await ChurnAPI.healthCheck();
        setStatus('connected', 'API Connected');

        // Load all data concurrently
        const [
            overview,
            churnDist,
            demographics,
            services,
            contracts,
            tenure,
            charges,
            modelPerf,
            featureImp,
            riskSegments
        ] = await Promise.all([
            ChurnAPI.getOverview(),
            ChurnAPI.getChurnDist(),
            ChurnAPI.getDemographics(),
            ChurnAPI.getServices(),
            ChurnAPI.getContracts(),
            ChurnAPI.getTenure(),
            ChurnAPI.getCharges(),
            ChurnAPI.getModelPerformance(),
            ChurnAPI.getFeatureImportance(),
            ChurnAPI.getRiskSegments()
        ]);

        // Render everything
        renderKPIs(overview);
        renderChurnDistChart(churnDist);
        renderRiskSegmentChart(riskSegments);
        renderTenureChart(tenure);
        renderContractChart(contracts.contract);
        renderPaymentChart(contracts.payment_method);
        renderInternetChart(services.InternetService);
        renderChargesChart(charges);
        renderGenderChart(demographics.gender);
        renderSeniorChart(demographics.SeniorCitizen);
        renderModelCards(modelPerf);
        renderFeatureChart(featureImp);
        renderRadarChart(modelPerf.models);

        // Hide loading overlay
        overlay.classList.add('hidden');
        setTimeout(() => overlay.style.display = 'none', 500);

    } catch (error) {
        console.error('Failed to initialize dashboard:', error);
        setStatus('error', 'API Error');
        overlay.querySelector('.loader-text').textContent =
            '⚠️ Could not connect to API. Make sure the backend is running on port 5000.';
        overlay.querySelector('.loader-ring').style.borderTopColor = '#ef4444';
    }

    // Setup event listeners
    setupNavigation();
    setupPredictForm();
}

// ---- KPI Rendering ----
function renderKPIs(data) {
    animateValue('kpi-total-value', 0, data.total_customers, 1200);
    animateValue('kpi-churned-value', 0, data.churned_customers, 1200);
    animateValue('kpi-retained-value', 0, data.retained_customers, 1200);
    animateValue('kpi-rate-value', 0, data.churn_rate, 1200, '%');
    animateValue('kpi-tenure-value', 0, data.avg_tenure, 1200);
    animateValue('kpi-monthly-value', 0, data.avg_monthly_charges, 1200, '', '$');

    // Animate bars
    setTimeout(() => {
        setBarWidth('kpi-churned-bar', data.churn_rate);
        setBarWidth('kpi-retained-bar', 100 - data.churn_rate);
        setBarWidth('kpi-rate-bar', data.churn_rate);
        setBarWidth('kpi-tenure-bar', (data.avg_tenure / 72) * 100);
        setBarWidth('kpi-monthly-bar', (data.avg_monthly_charges / 120) * 100);
    }, 200);
}

function animateValue(id, start, end, duration, suffix = '', prefix = '') {
    const el = document.getElementById(id);
    if (!el) return;

    const isFloat = !Number.isInteger(end);
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        const current = start + (end - start) * eased;

        el.textContent = prefix + (isFloat ? current.toFixed(1) : Math.round(current).toLocaleString()) + suffix;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

function setBarWidth(id, pct) {
    const el = document.getElementById(id);
    if (el) el.style.width = Math.min(pct, 100) + '%';
}

// ---- Model Cards ----
function renderModelCards(perfData) {
    const grid = document.getElementById('model-grid');
    grid.innerHTML = '';

    const models = perfData.models;
    const bestModel = perfData.best_model;

    for (const [name, metrics] of Object.entries(models)) {
        const isBest = name === bestModel;
        const card = document.createElement('div');
        card.className = `model-card${isBest ? ' best-model' : ''}`;

        const colorClass = (val) => val >= 80 ? 'high' : val >= 60 ? 'medium' : 'low';

        card.innerHTML = `
            <div class="model-name">${name}</div>
            <div class="model-metrics">
                <div class="metric-item">
                    <span class="metric-label">Accuracy</span>
                    <span class="metric-value ${colorClass(metrics.accuracy)}">${metrics.accuracy}%</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Precision</span>
                    <span class="metric-value ${colorClass(metrics.precision)}">${metrics.precision}%</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Recall</span>
                    <span class="metric-value ${colorClass(metrics.recall)}">${metrics.recall}%</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">F1 Score</span>
                    <span class="metric-value ${colorClass(metrics.f1_score)}">${metrics.f1_score}%</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">ROC AUC</span>
                    <span class="metric-value ${colorClass(metrics.roc_auc || 0)}">${metrics.roc_auc || '—'}%</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">True Pos.</span>
                    <span class="metric-value">${metrics.confusion_matrix.true_positive}</span>
                </div>
            </div>
        `;

        grid.appendChild(card);
    }
}

// ---- Navigation ----
function setupNavigation() {
    const links = document.querySelectorAll('.nav-link');
    links.forEach(link => {
        link.addEventListener('click', (e) => {
            links.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });

    // Update active link on scroll
    const sections = document.querySelectorAll('.section');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                links.forEach(l => {
                    l.classList.toggle('active', l.dataset.section === id);
                });
            }
        });
    }, { threshold: 0.3 });

    sections.forEach(s => observer.observe(s));
}

// ---- Predictor Form ----
function setupPredictForm() {
    const form = document.getElementById('predict-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const btn = document.getElementById('predict-btn');
        const btnText = btn.querySelector('.btn-text');
        const btnLoading = btn.querySelector('.btn-loading');

        btnText.style.display = 'none';
        btnLoading.style.display = 'inline';
        btn.disabled = true;

        try {
            // Collect form data
            const formData = new FormData(form);
            const customerData = {};
            for (const [key, value] of formData.entries()) {
                customerData[key] = parseFloat(value);
            }

            const result = await ChurnAPI.predict(customerData);
            showPredictionResult(result);
        } catch (error) {
            console.error('Prediction failed:', error);
        } finally {
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
            btn.disabled = false;
        }
    });
}

function showPredictionResult(result) {
    const card = document.getElementById('prediction-result');
    card.style.display = 'block';

    // Prediction text
    const predEl = document.getElementById('result-prediction');
    predEl.textContent = result.prediction;
    predEl.className = `result-prediction ${result.prediction === 'Churn' ? 'churn' : 'no-churn'}`;

    // Gauge
    const gaugeFill = document.getElementById('gauge-fill');
    const gaugeText = document.getElementById('gauge-text');
    const prob = result.churn_probability;

    gaugeFill.style.width = '0%';
    gaugeFill.className = 'gauge-fill';

    if (prob >= 70) gaugeFill.classList.add('high-risk');
    else if (prob >= 30) gaugeFill.classList.add('medium-risk');

    setTimeout(() => {
        gaugeFill.style.width = prob + '%';
        gaugeText.textContent = prob + '%';
    }, 100);

    // Risk badge
    const badge = document.getElementById('risk-badge');
    badge.textContent = result.risk_level + ' Risk';
    badge.className = `risk-badge ${result.risk_level.toLowerCase()}`;

    // Scroll into view
    card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ---- Status ----
function setStatus(state, text) {
    const dot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status-text');

    dot.className = `status-dot ${state}`;
    statusText.textContent = text;
}
