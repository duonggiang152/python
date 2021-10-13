function loadData() {
            document.getElementsByClassName("box-province")[0].innerHTML += `<div class = "province-content"><div>Tỉnh</div><div>Ca nhiễm</div></div>`
            fetch('./data-frist-block')
            .then(response => response.json())
            .then(data =>{    
                console.log(data.length)
                for(let i = 0; i < data.length; i++ ){
                    document.getElementsByClassName("box-province")[0].innerHTML += `<div class = "province-content"><div>${data[i].name}</div><div>${data[i].cases}</div></div>`
                }
                console.log(document.getElementsByClassName("box-province")[0])
            })
        }
window.addEventListener("load", () => {
    loadData()
})