let url = '/inventory/get_items_cate';
let data;

fetch(url)
    .then(res => res.json())
    .then(res => data = res)
    .catch(err => { throw err });

let getAllElement = () => {
    res = []
    for(let index in data){
        data[index].forEach(e => {
            res.push(e);
        })
    }
    res = res.sort((a, b) => {
            return a.id > b.id ? 1 : -1;
        });
    return res;
}

let changeOption = (id) => {
    // let cate = document.getElementById("id_form-0-category");
    // let item = document.getElementById("id_form-0-item");
    let cate = document.getElementById(id + "-category");
    let item = document.getElementById(id + "-item");
    let index = cate.options[cate.selectedIndex].value;
    let arr = data[index];
    if(arr === undefined){
        arr = getAllElement();
    }
    item.innerHTML = "";
    let content = "";
    for(let i=0; i<arr.length; i++)
        content += `<option value=${arr[i].id}>${arr[i].name}</option>`;
    item.innerHTML = content;
}

let resetAllOption = (total) => {
    for(let i=0; i<total; i++){
        document.getElementById(`id_form-${i}-category`)
        .addEventListener("change", () => {
            changeOption(`id_form-${i}`);
        });
    }
}

// resetAllOption(0);
document.getElementById("id_form-0-category")
        .addEventListener("change", () => {
            changeOption("id_form-0"); 
        });