let indexInit = () => {
    let list = [['year', 2010, 2019], ['month', 1, 12], ['day', 1, 31]]
    for(let i=0; i<list.length; i++){
        let parent = document.getElementById(list[i][0]);
        let child = document.createElement('option');
        child.text = '---';
        parent.add(child);
        for(let j=list[i][1]; j<=list[i][2]; j++){
            let child = document.createElement('option');
            child.text = j;
            parent.add(child);
        }
    }
    drawChart(0,0,0);
}

let call = () => {
    let year = document.getElementById('year').value;
    let month = document.getElementById('month').value;
    let day = document.getElementById('day').value;
    if(year == '---') year = 0;
    if(month == '---') month = 0;
    if(day == '---') day = 0;
    drawChart(year, month, day);
}

let drawChart = (year, month, day) => {
    fetch(`/inventory/get_statistic_data/${year}/${month}/${day}`)
    .then(res => res.json())
    .then(res => {
        let aspect = 2;
        if(window.bar !== undefined)
            window.bar.destroy();
        if(window.mobilecheck())
            aspect = 1;
        var ctx = document.getElementById('record').getContext('2d');
        window.bar = new Chart(ctx, {
            type: 'horizontalBar',
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            
            data: {
                labels: res['label'],
                datasets: [
                    {
                        label: "出貨",
                        backgroundColor: "rgba(255, 99, 132, 0.2)",
                        borderColor: 'rgba(255,99,132,1)',
                        data: res['SendRecord'],
                        borderWidth: 1,
                    },
                    {
                        label: "進貨",
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        data: res['ReceiveRecord'],
                        borderWidth: 1,
                    },
                    {
                        label: "庫存",
                        backgroundColor: 'rgba(255, 206, 86, 0.2)',
                        borderColor: 'rgba(255, 206, 86, 1)',
                        data: res['Resource'],
                        borderWidth: 1,
                    },
                ]
            },
            options: {
                aspectRatio: aspect,
                barValueSpacing: 20,
                scales: {xAxes: [{ ticks: { min: 0 }}]}
            }
        });
    });
}

let dateInit = () => {
    let today = new Date();
    today.setMonth(today.getMonth() + 1);
    let dateStr = today.toLocaleDateString().replace("/","-").replace("/","-");
    document.getElementsByTagName('input')[0].value = dateStr;
    dateHandler();
}

function dateHandler(e){
    let date = null;
    if (e === undefined){
        let today = new Date();
        today.setMonth(today.getMonth() + 1);
        date = today.toLocaleDateString().replace("/","-").replace("/","-");
    }
    else{
        date = e.target.value;
    }
    let tbl = "";
    let keys = ["物品名稱", "數量", "有效日期", "據點"];
    fetch(`/inventory/get_expired/${date}`)
        .then(res => res.json())
        .then(res => {
            res.forEach(element => {
                tbl += "<tr>"
                keys.forEach(key => {
                    if(key === "數量")
                        tbl += `<td>${element[key]} ${element["measure"]}</td>`
                    else
                        tbl += `<td>${element[key]}</td>`
                });
                tbl += "</tr>"
            });
            document.getElementById('expBody').innerHTML = tbl;
        });
}

indexInit();
dateInit();
// dateHandler();
// new Chart(document.getElementById("line-chart"), {
//   type: 'line',
//   data: {
//     labels: [1500,1600,1700,1750,1800,1850,1900,1950,1999,2050],
//     datasets: [{ 
//         data: [86,114,106,106,107,111,133,221,783,2478],
//         label: "Africa",
//         borderColor: "#3e95cd",
//         fill: false
//       }, { 
//         data: [282,350,411,502,635,809,947,1402,3700,5267],
//         label: "Asia",
//         borderColor: "#8e5ea2",
//         fill: false
//       }, { 
//         data: [168,170,178,190,203,276,408,547,675,734],
//         label: "Europe",
//         borderColor: "#3cba9f",
//         fill: false
//       }, { 
//         data: [40,20,10,16,24,38,74,167,508,784],
//         label: "Latin America",
//         borderColor: "#e8c3b9",
//         fill: false
//       }, { 
//         data: [6,3,2,2,7,26,82,172,312,433],
//         label: "North America",
//         borderColor: "#c45850",
//         fill: false
//       }
//     ]
//   },
//   options: {
//     title: {
//       display: true,
//       text: 'World population per region (in millions)'
//     }
//   }
// });



