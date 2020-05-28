function loadChart(data, color, labels, id_chart, description){
  var chart = new Chart(document.getElementById(id_chart), {
  type: 'doughnut',
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
    title: {
      display: true,
      text: description
    }
  }
});
}
