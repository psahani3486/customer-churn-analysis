/**
 * Chart.js Visualization Module for ChurnScope Dashboard.
 * Creates and manages all dashboard charts.
 */

// Global Chart.js defaults for dark theme
Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.06)';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.padding = 16;
Chart.defaults.responsive = true;
Chart.defaults.maintainAspectRatio = false;

// Color palette
const COLORS = {
    violet: '#8b5cf6',
    teal: '#14b8a6',
    blue: '#3b82f6',
    pink: '#ec4899',
    amber: '#f59e0b',
    red: '#ef4444',
    green: '#22c55e',
    indigo: '#6366f1',
    cyan: '#06b6d4',
    orange: '#f97316',
    violetAlpha: 'rgba(139, 92, 246, 0.6)',
    tealAlpha: 'rgba(20, 184, 166, 0.6)',
    blueAlpha: 'rgba(59, 130, 246, 0.6)',
    pinkAlpha: 'rgba(236, 72, 153, 0.6)',
    amberAlpha: 'rgba(245, 158, 11, 0.6)',
    redAlpha: 'rgba(239, 68, 68, 0.6)',
    greenAlpha: 'rgba(34, 197, 94, 0.6)',
};

const CHART_COLORS_LIST = [
    COLORS.violet, COLORS.teal, COLORS.blue, COLORS.pink,
    COLORS.amber, COLORS.indigo, COLORS.cyan, COLORS.orange
];

const CHART_COLORS_ALPHA = [
    COLORS.violetAlpha, COLORS.tealAlpha, COLORS.blueAlpha, COLORS.pinkAlpha,
    COLORS.amberAlpha, 'rgba(99, 102, 241, 0.6)', 'rgba(6, 182, 212, 0.6)', 'rgba(249, 115, 22, 0.6)'
];

// Store chart instances for cleanup
const chartInstances = {};

function destroyChart(id) {
    if (chartInstances[id]) {
        chartInstances[id].destroy();
        delete chartInstances[id];
    }
}

/**
 * Churn Distribution — Doughnut Chart
 */
function renderChurnDistChart(data) {
    destroyChart('churnDistChart');
    const ctx = document.getElementById('churnDistChart').getContext('2d');

    // Create gradient fills
    const gradientRed = ctx.createLinearGradient(0, 0, 0, 300);
    gradientRed.addColorStop(0, 'rgba(239, 68, 68, 0.8)');
    gradientRed.addColorStop(1, 'rgba(236, 72, 153, 0.8)');

    const gradientGreen = ctx.createLinearGradient(0, 0, 0, 300);
    gradientGreen.addColorStop(0, 'rgba(34, 197, 94, 0.8)');
    gradientGreen.addColorStop(1, 'rgba(20, 184, 166, 0.8)');

    chartInstances['churnDistChart'] = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: [gradientGreen, gradientRed],
                borderColor: ['rgba(34, 197, 94, 0.3)', 'rgba(239, 68, 68, 0.3)'],
                borderWidth: 2,
                hoverOffset: 12,
            }]
        },
        options: {
            cutout: '65%',
            plugins: {
                legend: { position: 'bottom' },
                tooltip: {
                    callbacks: {
                        label: (ctx) => `${ctx.label}: ${ctx.parsed} (${data.percentages[ctx.dataIndex]}%)`
                    }
                }
            }
        }
    });
}

/**
 * Risk Segments — Doughnut Chart
 */
function renderRiskSegmentChart(data) {
    destroyChart('riskSegmentChart');
    const ctx = document.getElementById('riskSegmentChart').getContext('2d');

    chartInstances['riskSegmentChart'] = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['High Risk', 'Medium Risk', 'Low Risk'],
            datasets: [{
                data: [data.high, data.medium, data.low],
                backgroundColor: [
                    'rgba(239, 68, 68, 0.75)',
                    'rgba(245, 158, 11, 0.75)',
                    'rgba(34, 197, 94, 0.75)'
                ],
                borderColor: [
                    'rgba(239, 68, 68, 0.3)',
                    'rgba(245, 158, 11, 0.3)',
                    'rgba(34, 197, 94, 0.3)'
                ],
                borderWidth: 2,
                hoverOffset: 12,
            }]
        },
        options: {
            cutout: '65%',
            plugins: {
                legend: { position: 'bottom' },
                tooltip: {
                    callbacks: {
                        label: (ctx) => {
                            const pcts = [data.high_pct, data.medium_pct, data.low_pct];
                            return `${ctx.label}: ${ctx.parsed} (${pcts[ctx.dataIndex]}%)`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Tenure Analysis — Line Chart
 */
function renderTenureChart(data) {
    destroyChart('tenureChart');
    const ctx = document.getElementById('tenureChart').getContext('2d');

    const gradient = ctx.createLinearGradient(0, 0, 0, 350);
    gradient.addColorStop(0, 'rgba(139, 92, 246, 0.3)');
    gradient.addColorStop(1, 'rgba(139, 92, 246, 0.01)');

    chartInstances['tenureChart'] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Churn Rate (%)',
                data: data.churn_rates,
                borderColor: COLORS.violet,
                backgroundColor: gradient,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: COLORS.violet,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 9,
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Churn Rate (%)' },
                    grid: { color: 'rgba(255,255,255,0.04)' }
                },
                x: {
                    title: { display: true, text: 'Tenure (months)' },
                    grid: { display: false }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

/**
 * Contract Type — Bar Chart
 */
function renderContractChart(data) {
    destroyChart('contractChart');
    const ctx = document.getElementById('contractChart').getContext('2d');

    chartInstances['contractChart'] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Retained',
                    data: data.retained,
                    backgroundColor: 'rgba(34, 197, 94, 0.7)',
                    borderRadius: 6,
                },
                {
                    label: 'Churned',
                    data: data.churned,
                    backgroundColor: 'rgba(239, 68, 68, 0.7)',
                    borderRadius: 6,
                }
            ]
        },
        options: {
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.04)' } },
                x: { grid: { display: false } }
            },
            plugins: {
                legend: { position: 'top' }
            }
        }
    });
}

/**
 * Payment Method — Horizontal Bar
 */
function renderPaymentChart(data) {
    destroyChart('paymentChart');
    const ctx = document.getElementById('paymentChart').getContext('2d');

    chartInstances['paymentChart'] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Retained',
                    data: data.retained,
                    backgroundColor: 'rgba(20, 184, 166, 0.7)',
                    borderRadius: 6,
                },
                {
                    label: 'Churned',
                    data: data.churned,
                    backgroundColor: 'rgba(236, 72, 153, 0.7)',
                    borderRadius: 6,
                }
            ]
        },
        options: {
            indexAxis: 'y',
            scales: {
                x: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.04)' } },
                y: { grid: { display: false } }
            },
            plugins: {
                legend: { position: 'top' }
            }
        }
    });
}

/**
 * Internet Service — Bar Chart
 */
function renderInternetChart(data) {
    destroyChart('internetChart');
    const ctx = document.getElementById('internetChart').getContext('2d');

    chartInstances['internetChart'] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Retained',
                    data: data.retained,
                    backgroundColor: 'rgba(59, 130, 246, 0.7)',
                    borderRadius: 6,
                },
                {
                    label: 'Churned',
                    data: data.churned,
                    backgroundColor: 'rgba(245, 158, 11, 0.7)',
                    borderRadius: 6,
                }
            ]
        },
        options: {
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.04)' } },
                x: { grid: { display: false } }
            },
            plugins: {
                legend: { position: 'top' }
            }
        }
    });
}

/**
 * Monthly Charges Comparison — Bar Chart
 */
function renderChargesChart(data) {
    destroyChart('chargesChart');
    const ctx = document.getElementById('chargesChart').getContext('2d');

    chartInstances['chargesChart'] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Mean', 'Median'],
            datasets: [
                {
                    label: 'Retained',
                    data: [data.monthly_charges.retained_mean, data.monthly_charges.retained_median],
                    backgroundColor: 'rgba(34, 197, 94, 0.7)',
                    borderRadius: 6,
                },
                {
                    label: 'Churned',
                    data: [data.monthly_charges.churned_mean, data.monthly_charges.churned_median],
                    backgroundColor: 'rgba(239, 68, 68, 0.7)',
                    borderRadius: 6,
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Monthly Charges ($)' },
                    grid: { color: 'rgba(255,255,255,0.04)' }
                },
                x: { grid: { display: false } }
            },
            plugins: {
                legend: { position: 'top' }
            }
        }
    });
}

/**
 * Gender — Doughnut
 */
function renderGenderChart(data) {
    destroyChart('genderChart');
    const ctx = document.getElementById('genderChart').getContext('2d');

    chartInstances['genderChart'] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Retained',
                    data: data.retained,
                    backgroundColor: 'rgba(99, 102, 241, 0.7)',
                    borderRadius: 6,
                },
                {
                    label: 'Churned',
                    data: data.churned,
                    backgroundColor: 'rgba(236, 72, 153, 0.7)',
                    borderRadius: 6,
                }
            ]
        },
        options: {
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.04)' } },
                x: { grid: { display: false } }
            },
            plugins: { legend: { position: 'top' } }
        }
    });
}

/**
 * Senior Citizen — Bar Chart
 */
function renderSeniorChart(data) {
    destroyChart('seniorChart');
    const ctx = document.getElementById('seniorChart').getContext('2d');

    chartInstances['seniorChart'] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Retained',
                    data: data.retained,
                    backgroundColor: 'rgba(6, 182, 212, 0.7)',
                    borderRadius: 6,
                },
                {
                    label: 'Churned',
                    data: data.churned,
                    backgroundColor: 'rgba(249, 115, 22, 0.7)',
                    borderRadius: 6,
                }
            ]
        },
        options: {
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.04)' } },
                x: { grid: { display: false } }
            },
            plugins: { legend: { position: 'top' } }
        }
    });
}

/**
 * Feature Importance — Horizontal Bar
 */
function renderFeatureChart(data) {
    destroyChart('featureChart');
    const ctx = document.getElementById('featureChart').getContext('2d');

    // Create gradient for each bar
    const colors = data.features.map((_, i) => {
        const t = i / data.features.length;
        return `rgba(${Math.round(139 - t * 80)}, ${Math.round(92 + t * 90)}, ${Math.round(246 - t * 80)}, 0.75)`;
    });

    chartInstances['featureChart'] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.features.map(f => f.replace(/_/g, ' ')),
            datasets: [{
                label: 'Importance',
                data: data.importances,
                backgroundColor: colors,
                borderRadius: 6,
            }]
        },
        options: {
            indexAxis: 'y',
            scales: {
                x: {
                    beginAtZero: true,
                    title: { display: true, text: 'Importance Score' },
                    grid: { color: 'rgba(255,255,255,0.04)' }
                },
                y: {
                    grid: { display: false },
                    ticks: { font: { size: 11 } }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

/**
 * Model Comparison — Radar Chart
 */
function renderRadarChart(modelData) {
    destroyChart('radarChart');
    const ctx = document.getElementById('radarChart').getContext('2d');

    const modelNames = Object.keys(modelData);
    const metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc'];
    const metricLabels = ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'ROC AUC'];

    const datasets = modelNames.map((name, i) => ({
        label: name,
        data: metrics.map(m => modelData[name][m] || 0),
        borderColor: CHART_COLORS_LIST[i],
        backgroundColor: CHART_COLORS_ALPHA[i].replace('0.6', '0.15'),
        borderWidth: 2,
        pointBackgroundColor: CHART_COLORS_LIST[i],
        pointRadius: 4,
    }));

    chartInstances['radarChart'] = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: metricLabels,
            datasets: datasets
        },
        options: {
            scales: {
                r: {
                    beginAtZero: false,
                    min: 40,
                    max: 100,
                    ticks: { stepSize: 10, backdropColor: 'transparent' },
                    grid: { color: 'rgba(255,255,255,0.06)' },
                    angleLines: { color: 'rgba(255,255,255,0.06)' },
                    pointLabels: { font: { size: 12, weight: 600 } }
                }
            },
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}
