document.addEventListener("DOMContentLoaded", () => {

    // Hard-coded mood colors
    const moodColors = {
        happy: "#fff0a7",
        sad: "#a6c4ff",
        energetic: "#ffa1a1",
        calm: "#9fd8cc"
    };

    fetch("/mood/data")
        .then(response => response.json())
        .then(data => {

            // Extract labels (mood names) and values (counts)
            const labels = Object.keys(data);
            const counts = Object.values(data);

            // Match each mood with its assigned color
            const backgroundColors = labels.map(
                mood => moodColors[mood] || "#888"
            );

            const ctx = document.getElementById("moodChart").getContext("2d");

            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Mood Count",
                        data: counts,
                        backgroundColor: backgroundColors,
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });
        });
});