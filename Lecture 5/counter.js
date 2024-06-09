if (!localStorage.getItem('counter')){
    localStorage.setItem('counter', 0);
}


function count() {
    let counter = localStorage.getItem('counter');
    counter++;
    document.querySelector('h1').innerHTML = counter;
    localStorage.setItem('counter', counter);

    // if (counter % 5 === 0) {
    //     alert(`Counter is now ${counter}`);
    // }
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('button').onclick = count;
    document.querySelector('h1').innerHTML = localStorage.getItem('counter')
    // setInterval(count, 1000);
})
