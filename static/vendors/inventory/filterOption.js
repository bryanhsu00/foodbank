let data;
let personData;

fetch('/inventory/get_items_cate')
    .then(res => res.json())
    .then(res => data = res)
    .catch(err => { throw err });

let getAllElement = () => {
    let res = []
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

let giveOptions = (total) => {
    total --;
    let item = document.getElementById(`id_form-${total}-item`);
    let arr = getAllElement();
    let content = "";
    for(let i=0; i<arr.length; i++)
        content += `<option value=${arr[i].id}>${arr[i].name}</option>`;
    item.innerHTML = content;
}

let changeOption = (id) => {
    let cate = document.getElementById(id + "-category");
    let item = document.getElementById(id + "-item");
    let index = cate.options[cate.selectedIndex].value;
    let arr = data[index];
    if(arr === undefined){
        arr = getAllElement();
    }
    let content = "";
    for(let i=0; i<arr.length; i++)
        content += `<option value=${arr[i].id}>${arr[i].name}</option>`;
    item.innerHTML = content;
}

let resetAllOption = (total) => { // formset中的form數量若有更動所有event需重新bind
    for(let i=0; i<total; i++){
        document.getElementById(`id_form-${i}-category`)
        .addEventListener("change", () => {
            changeOption(`id_form-${i}`);
        });
    }
}

let initRecord = () => {
    document.getElementById("id_form-0-category")
    .addEventListener("change", () => {
        changeOption("id_form-0"); 
    });
    let path = new URL(window.location.href).pathname.split("/")[3];
    let model;
    if(path === 'ReceiveRecord')
        model = 'donator';
    else
        model = 'household';
    fetch(`/inventory/api/${model.charAt(0).toUpperCase() + model.slice(1)}`)
        .then(res => res.json())
        .then(res => {
            personData = res;
            let before = document.getElementById(`id_${model}`);
            let after = document.createElement('input');
            let l = before.attributes;
            for(let i=0; i<l.length; i++){
                if(l[i].name !== 'style')
                    after.setAttribute(l[i].name, l[i].value);
            }
            after.setAttribute('list', `${model}s`);
            after.setAttribute('autocomplete', 'off');
            before.parentNode.replaceChild(after, before);
            let dataList = document.createElement('datalist');
            dataList.setAttribute('id', `${model}s`);
            personData.forEach(element => {
                let option = document.createElement('option')
                option.value = element.name;
                dataList.appendChild(option);
            });
            after.parentElement.appendChild(dataList);
            if(name !== ''){
                after.value = name;
            }
        })
        .catch(err => { throw err });
}

initRecord();