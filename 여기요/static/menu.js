async function changeDom() {
    let votes = document.querySelector('form')
    let data = await fetch('http://192.168.35.78:5000/vote2/').then(res=> res.json()).then(result => result)
    votes.innerHTML = `
        <option value="" selected="">투표 하세요.</option>
        <input type="radio" name="${data.list[0]}" value="${data.list[0]}">
        <input type="radio" name="${data.list[1]}" value="${data.list[1]}">
    `
}

let button = document.querySelector('button')
button.addEventListener('click', function() {
    changeDom()
})