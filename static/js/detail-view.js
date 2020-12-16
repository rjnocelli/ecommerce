import { addLoQuieroTag } from './functions.js'
(function(){
    console.log('detail-view js working')
    const products = JSON.parse(localStorage.getItem('products'))
    const mydata = JSON.parse(document.getElementById('mydata').textContent);
    console.log(mydata)

    const producto = products.filter(p =>{
    return p.id === mydata;
    });

    addLoQuieroTag(producto, 'lo-quiero')
})();

