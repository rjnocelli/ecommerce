import { addLoQuieroTag } from './functions.js'
console.log('detail-view js working')

(function(){
    const products = JSON.parse(localStorage.getItem('products'))
    const mydata = JSON.parse(document.getElementById('mydata').textContent);

    const producto = products.filter(p =>{
    return p.id === mydata;
    });

    addLoQuieroTag(producto, 'lo-quiero')
}());

