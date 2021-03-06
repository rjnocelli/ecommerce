import { addProductOrCreateOrder } from './functions.js'
(function(){
    console.log('detail-view js working')
    const products = JSON.parse(localStorage.getItem('products'))
    const mydata = JSON.parse(document.getElementById('mydata').textContent);

    const getProductFromId = (product_id) => {
        return products.filter((p) => {
            return p ? p.id === product_id : null
        });
    };

    const product = getProductFromId(mydata)[0]

    const lo_quiero_button = document.getElementById("lo-quiero-button")
    lo_quiero_button.addEventListener("click", (e) => {
        e.preventDefault()
        addProductOrCreateOrder(product)
    });
})();

