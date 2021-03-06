import { addProductOrCreateOrder } from './functions.js'
(function(){
    console.log('detail-view js working')
    const product = JSON.parse(document.getElementById('product_data').textContent)
    const lo_quiero_button = document.getElementById("lo-quiero-button")
    lo_quiero_button.addEventListener("click", (e) => {
        e.preventDefault()
        addProductOrCreateOrder(product)
    });
})();

