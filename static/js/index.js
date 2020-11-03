console.log('index.js loaded yeahhh...')   

const updateCart = () =>{
    cart = document.querySelector('#cart span')
    cart.innerHTML = ` `
    cart.innerHTML = ` ${total_quantity} `

}
    function updateLocalStorage(){
        localStorage.setItem('order', JSON.stringify(order))
        localStorage.setItem('total_quantity', JSON.stringify(total_quantity))
        localStorage.setItem('total_price', JSON.stringify(total_price))
    }
    
    const addLoQuieroTag = (products, first_half_id) => {
        products.forEach((product) => {
            lo_quiero_atag = document.getElementById(`${first_half_id} ${product.id}`)
            lo_quiero_atag.addEventListener('click', (a) => {
                a.preventDefault()
                addProductOrCreateOrder(product)
            });
    
        });
    }

    const addProductOrCreateOrder = (product) => {
        if(localStorage.getItem('total_price') && localStorage.getItem('total_quantity')){
            total_quantity = parseInt(localStorage.getItem('total_quantity'))
            total_price = parseInt(localStorage.getItem('total_price'))
            console.log('ya existe orden, quantity y price')
        }else{
            total_quantity = 0
            total_price = 0
            console.log('creando variables')
        }
        if(localStorage.getItem('order')){
            order = JSON.parse(localStorage.getItem('order'))
                if(order[product.name]){
                    order[product.name].quantity += 1 
                }else{
                    order[product.name] = {'id':product.id,'name':product.name,'price':product.price,'quantity':1}
                }
        }else{
            order = {}
            order[product.name] = {'id':product.id,'name':product.name,'price':product.price,'quantity':1}
        }
    total_quantity += 1
    total_price += parseInt(product.price)
    updateCart()
    updateLocalStorage()
    let message = document.querySelector('#add-item-message')
    message.classList.add('show')
    };

    buildProductsList()
    buildMostPouplarProductsList()

    function buildMostPouplarProductsList(){
        const url = '/api/popular-products/'

        fetch(url)
            .then(function(response){ return response.json() })
            .then(fetchMostPopularProducts)
    }

    function buildProductsList(){
		const url = '/api/product-list/'

		fetch(url)
			.then(function(response) { return response.json(); })
            .then(updateProducts);
    
        }

    function fetchMostPopularProducts(products){
        popular_products_div = document.getElementById('most-popular')
        popular_products_div.innerHTML = ``
        products.forEach((product) => {
            popular_products_div.innerHTML += `
            <div id='popular-product ${product.id}' class=" p-3 col-lg-3 col-md-3 col-sm-3">
                <a href=""><img class="img-thumbnail" src="${product.image}"></a>
                <div class="box-element product p-3">
                    <h6 class="pt-2" style="display: inline-block; float: right">$ ${product.price}</h6>
                    <a href=""><h6 class="pt-2" style="display: inline-block"><strong>${product.name}</strong></h6></a>
                    <br><a id='lo-quiero-mp ${product.id}' class="btn btn-success btn-sm" href="">Lo Quiero</a> 
                </div>
                <br>
            </div>
            `
        });
    
    addLoQuieroTag(products, "lo-quiero-mp")

    }

    function updateProducts(products){
        console.log(products)
        localStorage.setItem('products', JSON.stringify(products))
        
        renderProducts(products)

        addLoQuieroTag(products, "lo-quiero")

        function renderProducts(products) {
            products_row = document.getElementById('product-details');
            products.forEach((product) => {
                products_row.innerHTML += `
                <div class="col-lg-3 col-md-3 col-sm-3">
                    <a href=""><img class="img-thumbnail" src=${product.image}></a>
                    <div class="box-element product">
                        <a href=""><h6 class="pt-2" style="display: inline-block"><strong>${product.name}</strong></h6></a>
                        <h6 class="pt-2" style="display: inline-block; float:right">$ ${product.price}</h6>				
                        <br><a id='lo-quiero ${product.id}' class="btn btn-success btn-sm" href="">Lo Quiero</a>
                    </div>
                    <br>
                </div>
                `
            });
        };

    };
    