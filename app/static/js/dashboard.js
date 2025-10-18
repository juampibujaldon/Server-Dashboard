(function () {
    const rawData = typeof DASHBOARD_DATA === "string" ? JSON.parse(DASHBOARD_DATA) : DASHBOARD_DATA;
    const data = rawData || {};

    const summaryEls = document.querySelectorAll("[data-summary]");
    const serversContainer = document.getElementById("serversContainer");
    const selector = document.getElementById("serverSelector");
    const statusCanvas = document.getElementById("statusChart");
    const trendCanvas = document.getElementById("trendChart");

    if (!summaryEls.length || !statusCanvas || !trendCanvas || !serversContainer || !selector) {
        console.warn("Dashboard layout is missing expected elements.");
        return;
    }

    const summary = data.summary || {};
    const servers = Array.isArray(data.servers) ? data.servers : [];
    const statusCounts = data.statusCounts || {};

    const numberFormat = new Intl.NumberFormat("es-AR", { maximumFractionDigits: 0 });
    const decimalFormat = new Intl.NumberFormat("es-AR", { maximumFractionDigits: 2 });
    const datetimeFormat = new Intl.DateTimeFormat("es-AR", {
        dateStyle: "short",
        timeStyle: "short",
    });

    function formatValue(value, options = {}) {
        if (value === null || value === undefined || Number.isNaN(value)) {
            return "—";
        }
        if (options.type === "decimal") {
            return decimalFormat.format(value);
        }
        return numberFormat.format(value);
    }

    function renderSummary() {
        summaryEls.forEach((element) => {
            const key = element.getAttribute("data-summary");
            const value = summary[key];
            const isDecimal =
                ["avgCpu", "avgRam", "avgDisk", "avgTemperature"].indexOf(key) !== -1;
            element.textContent = formatValue(value, { type: isDecimal ? "decimal" : "integer" });
        });
    }

    function renderServerCards() {
        if (!servers.length) {
            serversContainer.innerHTML =
                '<p class="servers__empty">Aún no hay métricas registradas. Envía datos a la API para comenzar.</p>';
            return;
        }

        const fragments = servers.map((server) => {
            const latest = server.latest || {};
            const averages = server.averages || {};
            const capturedAt = latest.capturedAt ? new Date(latest.capturedAt) : null;
            const statusClass = `status-pill status-pill--${server.status || "ok"}`;

            return `
                <article class="server-card">
                    <header class="server-card__header">
                        <span class="server-card__id">${server.serverId}</span>
                        <span class="${statusClass}">${(server.status || "ok").toUpperCase()}</span>
                    </header>
                    <div class="server-card__body">
                        <div class="server-card__metric">
                            <span>CPU actual</span>
                            <span>${formatValue(latest.cpu, { type: "decimal" })}%</span>
                        </div>
                        <div class="server-card__metric">
                            <span>RAM actual</span>
                            <span>${formatValue(latest.ram, { type: "decimal" })}%</span>
                        </div>
                        <div class="server-card__metric">
                            <span>Disco actual</span>
                            <span>${formatValue(latest.disk, { type: "decimal" })}%</span>
                        </div>
                        <div class="server-card__metric">
                            <span>Temperatura</span>
                            <span>${formatValue(latest.temperature, { type: "decimal" })}°C</span>
                        </div>
                        <hr class="server-card__divider" aria-hidden="true" />
                        <div class="server-card__metric">
                            <span>CPU promedio</span>
                            <span>${formatValue(averages.cpu, { type: "decimal" })}%</span>
                        </div>
                        <div class="server-card__metric">
                            <span>RAM promedio</span>
                            <span>${formatValue(averages.ram, { type: "decimal" })}%</span>
                        </div>
                        <div class="server-card__metric">
                            <span>Disco promedio</span>
                            <span>${formatValue(averages.disk, { type: "decimal" })}%</span>
                        </div>
                        <div class="server-card__metric">
                            <span>Temperatura promedio</span>
                            <span>${formatValue(averages.temperature, { type: "decimal" })}°C</span>
                        </div>
                    </div>
                    <footer class="server-card__footer">
                        Último reporte: ${
                            capturedAt ? datetimeFormat.format(capturedAt) : "sin datos"
                        }
                    </footer>
                </article>
            `;
        });

        serversContainer.innerHTML = fragments.join("\n");
    }

    function createStatusChart() {
        const dataset = {
            labels: ["En buen estado", "Requiere atención", "Crítico"],
            values: [
                statusCounts.ok || 0,
                statusCounts.warning || 0,
                statusCounts.critical || 0,
            ],
        };

        return new Chart(statusCanvas.getContext("2d"), {
            type: "doughnut",
            data: {
                labels: dataset.labels,
                datasets: [
                    {
                        data: dataset.values,
                        backgroundColor: ["#22c55e", "#facc15", "#f87171"],
                        borderWidth: 0,
                        hoverOffset: 8,
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            color: "#e2e8f0",
                            boxWidth: 16,
                            padding: 18,
                        },
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const value = context.formattedValue;
                                const label = context.label || "";
                                return `${label}: ${value}`;
                            },
                        },
                    },
                },
            },
        });
    }

    function buildTrendDataset(server) {
        const trend = Array.isArray(server.trend) ? server.trend : [];
        const labels = trend.map((entry) =>
            entry.capturedAt ? datetimeFormat.format(new Date(entry.capturedAt)) : ""
        );
        return {
            labels,
            datasets: [
                {
                    label: "CPU (%)",
                    data: trend.map((entry) => entry.cpu ?? null),
                    borderColor: "#38bdf8",
                    tension: 0.35,
                    fill: false,
                },
                {
                    label: "RAM (%)",
                    data: trend.map((entry) => entry.ram ?? null),
                    borderColor: "#c084fc",
                    tension: 0.35,
                    fill: false,
                },
                {
                    label: "Disco (%)",
                    data: trend.map((entry) => entry.disk ?? null),
                    borderColor: "#fbbf24",
                    tension: 0.35,
                    fill: false,
                },
                {
                    label: "Temperatura (°C)",
                    data: trend.map((entry) => entry.temperature ?? null),
                    borderColor: "#f97316",
                    tension: 0.35,
                    fill: false,
                },
            ],
        };
    }

    let trendChartInstance = null;

    function renderTrendChart(server) {
        if (trendChartInstance) {
            trendChartInstance.destroy();
        }

        if (!server) {
            trendCanvas.classList.add("chart--empty");
            const ctx = trendCanvas.getContext("2d");
            ctx.clearRect(0, 0, trendCanvas.width, trendCanvas.height);
            return;
        }

        trendChartInstance = new Chart(trendCanvas.getContext("2d"), {
            type: "line",
            data: buildTrendDataset(server),
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        ticks: { color: "#94a3b8" },
                        grid: { color: "rgba(148, 163, 184, 0.15)" },
                    },
                    y: {
                        ticks: { color: "#94a3b8" },
                        grid: { color: "rgba(148, 163, 184, 0.15)" },
                        suggestedMin: 0,
                        suggestedMax: 100,
                    },
                },
                plugins: {
                    legend: {
                        labels: {
                            color: "#e2e8f0",
                            usePointStyle: true,
                        },
                    },
                    tooltip: {
                        mode: "index",
                        intersect: false,
                    },
                },
            },
        });
    }

    function hydrateSelector() {
        selector.innerHTML = "";

        if (!servers.length) {
            selector.disabled = true;
            selector.innerHTML = '<option value="">Sin datos</option>';
            renderTrendChart(null);
            return;
        }

        selector.disabled = false;
        servers.forEach((server, index) => {
            const option = document.createElement("option");
            option.value = server.serverId;
            option.textContent = `${server.serverId} (${server.status || "ok"})`;
            if (index === 0) {
                option.selected = true;
            }
            selector.appendChild(option);
        });

        renderTrendChart(servers[0]);

        selector.addEventListener("change", (event) => {
            const selectedId = event.target.value;
            const server = servers.find((item) => item.serverId === selectedId);
            renderTrendChart(server || null);
        });
    }

    renderSummary();
    hydrateSelector();
    renderServerCards();
    createStatusChart();
})();
