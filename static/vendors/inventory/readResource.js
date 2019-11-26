let lang = {
    "decimal":        "",
    "emptyTable":     "No data available in table",
    "info":           "_TOTAL_ 筆資料中的 _START_ 到 _END_ 筆",
    "infoEmpty":      "Showing 0 to 0 of 0 entries",
    "infoFiltered":   "(filtered from _MAX_ total entries)",
    "infoPostFix":    "",
    "thousands":      ",",
    "lengthMenu":     "顯示 _MENU_ 筆資料",
    "loadingRecords": "Loading...",
    "processing":     "Processing...",
    "search":         "搜尋 ",
    "zeroRecords":    "No matching records found",
    "paginate": {
        "first":      "First",
        "last":       "Last",
        "next":       "下一頁",
        "previous":   "上一頁"
    },
    "aria": {
        "sortAscending":  ": activate to sort column ascending",
        "sortDescending": ": activate to sort column descending"
    }
}

let loadData = () => {
    let location = document.getElementById('location').value;
    let cate = document.getElementById('cate').value;
    if(location === "") location = "None";
    if(cate === "") cate = "None";
    let url = `/inventory/get_resource/${location}/${cate}`
    fetch(url)
        .then(res => res.json())
        .then(res => {
            tbl.clear();
            tbl.rows.add(res.data);
            tbl.draw();
        });
}

let initDataTable = () => {
    tbl = $('#mytable').DataTable({
        destroy: true,
        "language": lang,
        "order": [],
        "ajax": "/inventory/get_resource/None/None",
        "columns": [
            { "data": "iname" },
            { "data": "rsum" },
            { "data": "rdate" },
        ]
    });
}

let initOptions = () => {
    let parent = document.querySelectorAll(".row")[0];
    let child = parent.querySelectorAll(".col-sm-12, .col-md-6");
    for(let i=0; i<child.length; i++){
        child[i].className ="col-sm-12 col-md-3";
    }
    parent.insertAdjacentHTML("beforeend", 
    `<div class='col-sm-12 col-md-3'>
        <label>
            倉庫 
            <select 
            class='custom-select custom-select-sm form-control form-control-sm'
            id='location'
            onchange='loadData()'>
            </select>
        </label>
    </div>
    <div class='col-sm-12 col-md-3'>
        <label>
            分類 
            <select 
            class='custom-select custom-select-sm form-control form-control-sm'
            id='cate'
            onchange='loadData()'>
            </select>
        </label>
    </div>`
    );

    [['Location', 'location'], ['Category', 'cate']].forEach(element => {
        fetch(`/inventory/api/${element[0]}`)
        .then(res => res.json())
        .then(res => {
            let optionStr = "<option value=''>-------</option>";
            for(let i=0; i<res.length; i++){
                optionStr += `<option value=${res[i].id}>${res[i].name}</option>`
            }
            document.getElementById(element[1]).innerHTML = optionStr;
        })
        .catch(err => { throw err });
    });
}

$(document).ready(function(){
    initDataTable();
    initOptions();
});