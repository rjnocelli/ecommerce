const addLoQuieroTag = (products, first_half_id) =>{
    console.log('addLoQuieroTag funciona')
    if(products.length > 1){
        products.forEach((product) => {
            lo_quiero_atag = document.getElementById(`${first_half_id} ${product.id}`)
            lo_quiero_atag.addEventListener('click', (event) => {
                event.preventDefault()
                addProductOrCreateOrder(product)
            });
        });
    
    }else if(products.length === 1){
        product = products[0]
        lo_quiero_atag = document.getElementById(`${first_half_id} ${product.id}`)
            lo_quiero_atag.addEventListener('click', (event) => {
                event.preventDefault()
                addProductOrCreateOrder(product)
            });
    }else{
        product = products
        lo_quiero_atag = document.getElementById(`${first_half_id} ${product.id}`)
            lo_quiero_atag.addEventListener('click', (event) => {
                event.preventDefault()
                addProductOrCreateOrder(product)
            });
    }
};

