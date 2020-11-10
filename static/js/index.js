console.log('index.js loaded yeahhh...')   

const renderDetailView = (product) => {
    const main_div = document.getElementById('main-div')
    main_div.innerHTML = ``
    main_div.innerHTML = `
    
    <div class="card mt-5 mb-5 mx-auto p-2" style="width: 20rem;">
        <img class="card-img-top img-thumbnail" src="${product.image}" alt="Card image cap">
        <div class="card-body">
        <h3>${product.name}</h3>
        <div id='cat-div'></div>
        <p>precio p/u: <span class='float-right'>$${product.price}</span></p>
        <hr>
        <p class="card-text">${product.description}</p>
        <a id='lo-quiero ${product.id}' class="btn btn-success">Lo Quiero! <span class='far fa-candy-cane'></span></a>
      </div>
  </div>`
  let cat_div = document.getElementById('cat-div')
  product.category.forEach((cat) => {
      cat_div.innerHTML += `<span class="badge badge-primary">${cat.name}</span>
      `
  })

  addLoQuieroTag(product, 'lo-quiero')  
  window.scrollTo(200,300)
  
}

const updateCart = () => {
    cart = document.querySelector('#cart span')
    cart.innerHTML = ` `
    cart.innerHTML = ` ${total_quantity} `

}
    function updateLocalStorage() {
        localStorage.setItem('order', JSON.stringify(order))
        localStorage.setItem('total_quantity', JSON.stringify(total_quantity))
        localStorage.setItem('total_price', JSON.stringify(total_price))
    }
    
    const addLoQuieroTag = (products, first_half_id) => {
        if(products.length > 1){
            products.forEach((product) => {
                lo_quiero_atag = document.getElementById(`${first_half_id} ${product.id}`)
                lo_quiero_atag.addEventListener('click', (event) => {
                    event.preventDefault()
                    addProductOrCreateOrder(product)
                });
            });
        
        }else{
            lo_quiero_atag = document.getElementById(`${first_half_id} ${products.id}`)
                lo_quiero_atag.addEventListener('click', (event) => {
                    event.preventDefault()
                    addProductOrCreateOrder(products)
                });
        } 
    };

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
    // let message = document.querySelector('#add-item-message')
    // message.classList.add('show')
    };

    buildProductsList()
    buildMostPouplarProductsList()

    function buildMostPouplarProductsList() {
        const url = '/api/popular-products/'

        fetch(url)
            .then(function(response){ return response.json() })
            .then(fetchMostPopularProducts)
    }

    function buildProductsList() {
		const url = '/api/product-list/'

		fetch(url)
			.then(function(response) { return response.json(); })
            .then(updateProducts);
    
        }

    function fetchMostPopularProducts(products) {
        popular_products_div = document.getElementById('most-popular')
        popular_products_div.innerHTML = ``
        products.forEach((product) => {
            popular_products_div.innerHTML += `
            <div id='popular-product ${product.id}' class=" p-3 col-lg-3 col-md-3 col-sm-3">
                <a id='img-atag-mp ${product.id}' href=""><img class="img-thumbnail" src="${product.image}"></a>
                <div class="box-element product p-3">
                    <h6 class="pt-2" style="display: inline-block; float: right">$ ${product.price}</h6>
                    <a href=""><h6 class="pt-2" style="display: inline-block"><strong>${product.name}</strong></h6></a>
                    <br><a id='lo-quiero-mp ${product.id}' class="btn btn-success btn-sm" href="">Lo Quiero! <span class='far fa-candy-cane'></span></a> 
                </div>
                <br>
            </div>
            `
        });
    
    addLoQuieroTag(products, "lo-quiero-mp")

    products.forEach((product)=> {
        const product_a_tag = document.getElementById('img-atag-mp '+ product.id)
        product_a_tag.addEventListener('click', ()=> {
            event.preventDefault()
            renderDetailView(product)
        });
    });

    }

    function updateProducts(products) {
        console.log(products)
        localStorage.setItem('products', JSON.stringify(products))
        
        renderProducts(products)

        addLoQuieroTag(products, "lo-quiero")

        function renderProducts(products) {
            products_row = document.getElementById('product-details');
            products.forEach((product) => {
                products_row.innerHTML += `
                <div class="col-lg-3 col-md-3 col-sm-3">
                    <a href=""><img id='img-atag ${product.id}' class="img-thumbnail" src=${product.image}></a>
                    <div class="box-element product">
                        <a href=""><h6 class="pt-2" style="display: inline-block"><strong>${product.name}</strong></h6></a>
                        <h6 class="pt-2" style="display: inline-block; float:right">$ ${product.price}</h6>				
                        <br><a id='lo-quiero ${product.id}' class="btn btn-success btn-sm" href="">Lo Quiero! <span class='far fa-candy-cane'></span></a>
                    </div>
                    <br>
                </div>
                `
            });

            products.forEach((product)=> {
                const product_a_tag = document.getElementById('img-atag '+ product.id)
                product_a_tag.addEventListener('click', ()=> {
                    event.preventDefault()
                    renderDetailView(product)
                });
            });

        };
    };
    