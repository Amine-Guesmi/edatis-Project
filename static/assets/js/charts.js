function loadChart(data, color, labels, id_chart, description, chart_type, display){
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
    legend: { display: display },
    title: {
      display: true,
      text: description
    }
  }
});
}
function loadBarChart(labels, title1, title2, data1, data2, id_chart, color1, color2, description){
  return new Chart(document.getElementById(id_chart), {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: title1,
          backgroundColor: color1,
          data: data1
        }, {
          label: title2,
          backgroundColor: color2,
          data: data2
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

function loadAnalysePerTimeChart(labels, data1, data2, data3, id, text) {
  return new Chart(document.getElementById(id), {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
          data: data1,
          label: "Clic",
          borderColor: "#3e95cd",
          fill: false
        }, {
          data: data2,
          label: "Open",
          borderColor: "#8e5ea2",
          fill: false
        }, {
          data: data3,
          label: "Recieved",
          borderColor: "#3cba9f",
          fill: false
        },
      ]
    },
    options: {
      title: {
        display: true,
        text: text
      }
    }
  });
}

// chart multiple
function loadChartMultiple(data1, data2, color, labels, id_chart, description, chart_type, display){
  return new Chart(document.getElementById(id_chart), {
  type: chart_type,
  data: {
    labels: labels,
    datasets: [
      {
        backgroundColor: color,
        data: data1
      },{
        backgroundColor: color,
        data:data2
      }
    ]
  },
  options: {
    legend: { display: display },
    title: {
      display: true,
      text: description
    }
  }
});
}
function loadBarChartmultiple(labels, title1, title2, titre3, data1, data2, data3, id_chart, color1, color2, color3, description){
  return new Chart(document.getElementById(id_chart), {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: title1,
          backgroundColor: color1,
          data: data1
        }, {
          label: title2,
          backgroundColor: color2,
          data: data2
        }, {
          label: titre3,
          backgroundColor: color3,
          data: data3
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
