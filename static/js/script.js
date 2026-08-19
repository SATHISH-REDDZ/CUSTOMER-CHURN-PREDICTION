/* -------------------------------------------------------------
   CUSTOMER CHURN PREDICTION SYSTEM - FRONTEND SCRIPT
   ------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', function () {
    // Initialize Lucide Icons if loaded
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // Handle TotalCharges calculation suggestion on Predict page
    const tenureInput = document.getElementById('tenure');
    const monthlyInput = document.getElementById('MonthlyCharges');
    const totalInput = document.getElementById('TotalCharges');

    if (tenureInput && monthlyInput && totalInput) {
        function updateTotalCharges() {
            const tenure = parseFloat(tenureInput.value) || 0;
            const monthly = parseFloat(monthlyInput.value) || 0;
            if (tenure > 0 && monthly > 0) {
                totalInput.value = (tenure * monthly).toFixed(2);
            }
        }
        tenureInput.addEventListener('input', updateTotalCharges);
        monthlyInput.addEventListener('input', updateTotalCharges);
    }
});

// Function to render Dashboard Charts
function initDashboardCharts(stats) {
    if (typeof Chart === 'undefined' || !stats) return;

    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Inter', sans-serif";

    // 1. Churn vs Retained Pie Chart
    const churnCtx = document.getElementById('churnDistChart');
    if (churnCtx) {
        new Chart(churnCtx, {
            type: 'doughnut',
            data: {
                labels: ['Retained Customers', 'Churned Customers'],
                datasets: [{
                    data: [stats.retained_count, stats.churned_count],
                    backgroundColor: ['#10b981', '#f43f5e'],
                    borderColor: '#0f172a',
                    borderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }

    // 2. Risk Distribution Chart
    const riskCtx = document.getElementById('riskDistChart');
    if (riskCtx) {
        new Chart(riskCtx, {
            type: 'bar',
            data: {
                labels: ['Low Risk (<30%)', 'Medium Risk (30-70%)', 'High Risk (≥70%)'],
                datasets: [{
                    label: 'Customer Count',
                    data: [stats.low_risk_count, stats.medium_risk_count, stats.high_risk_count],
                    backgroundColor: ['#10b981', '#f59e0b', '#f43f5e'],
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } },
                    x: { grid: { display: false } }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // 3. Contract Breakdown Chart
    const contractCtx = document.getElementById('contractDistChart');
    if (contractCtx) {
        const labels = Object.keys(stats.contract_dist || {});
        const data = Object.values(stats.contract_dist || {});
        new Chart(contractCtx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Predictions',
                    data: data,
                    backgroundColor: ['#6366f1', '#a855f7', '#06b6d4'],
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } },
                    x: { grid: { display: false } }
                },
                plugins: { legend: { display: false } }
            }
        });
    }
}

// Function to render Analytics Comparison Charts
function initAnalyticsCharts(metricsData) {
    if (typeof Chart === 'undefined' || !metricsData || !metricsData.metrics) return;

    Chart.defaults.color = '#94a3b8';

    const models = Object.keys(metricsData.metrics);
    const accuracy = models.map(m => (metricsData.metrics[m].accuracy * 100).toFixed(2));
    const precision = models.map(m => (metricsData.metrics[m].precision * 100).toFixed(2));
    const recall = models.map(m => (metricsData.metrics[m].recall * 100).toFixed(2));
    const f1 = models.map(m => (metricsData.metrics[m].f1_score * 100).toFixed(2));
    const rocAuc = models.map(m => (metricsData.metrics[m].roc_auc).toFixed(4));

    // 1. Model Comparison Multi-Bar Chart
    const compCtx = document.getElementById('modelComparisonChart');
    if (compCtx) {
        new Chart(compCtx, {
            type: 'bar',
            data: {
                labels: models,
                datasets: [
                    { label: 'Accuracy (%)', data: accuracy, backgroundColor: '#6366f1' },
                    { label: 'Precision (%)', data: precision, backgroundColor: '#06b6d4' },
                    { label: 'Recall (%)', data: recall, backgroundColor: '#f59e0b' },
                    { label: 'F1 Score (%)', data: f1, backgroundColor: '#a855f7' }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { min: 40, max: 100, grid: { color: 'rgba(255,255,255,0.05)' } },
                    x: { grid: { display: false } }
                },
                plugins: { legend: { position: 'bottom' } }
            }
        });
    }

    // 2. Feature Importance Horizontal Bar Chart
    const featCtx = document.getElementById('featureImportanceChart');
    if (featCtx && metricsData.feature_importances) {
        const featLabels = metricsData.feature_importances.map(f => f.feature);
        const featValues = metricsData.feature_importances.map(f => (f.importance * 100).toFixed(2));

        new Chart(featCtx, {
            type: 'bar',
            data: {
                labels: featLabels,
                datasets: [{
                    label: 'Feature Importance Score (%)',
                    data: featValues,
                    backgroundColor: '#06b6d4',
                    borderRadius: 6
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } },
                    y: { grid: { display: false } }
                },
                plugins: { legend: { display: false } }
            }
        });
    }
}
