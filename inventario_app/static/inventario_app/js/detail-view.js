import { addLoQuieroTag } from './functions.js'
(function(){
    console.log('detail-view js working')
    const products = JSON.parse(localStorage.getItem('products'))
    const mydata = JSON.parse(document.getElementById('mydata').textContent);

    const get_product_price = (product_id) => {
        let product_selected = products.filter((p) => {
            return p ? p.id === product_id : null
        });
        product_selected = product_selected[0];
        if(product_selected.sold_by_weight){
            const select_value = document.getElementById("price-by-weight-select-id").value
            return select_value.split(" ")[1]
        }else{
            return product_selected.price
        };
    };
    const lo_quiero_button = document.getElementById("lo-quiero-button")
    lo_quiero_button.addEventListener("click", (e) => {
        e.preventDefault()
        console.log(get_product_price(mydata))
    });
})();

