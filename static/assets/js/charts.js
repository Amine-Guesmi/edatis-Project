function loadChart(data, color, labels, id_chart, description, chart_type){
  return new Chart(document.getElementById(id_chart), {
  type: chart_type,
  data: {
    labels: labels,
    datasets: [
      {
        backgroundColor: color,
        data: data
      }
    ]
  },
  options: {
    legend: { display: false },
    title: {
      display: true,
      text: description
    }
  }
});
}
