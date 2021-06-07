import { addLoQuieroTag, updateCart, updateLocalStorage, addProductOrCreateOrder  } from './functions.js'
console.log('index.js working')

const fetchMostPopularProducts = (products) => {
    let carrousel_inner_div = document.querySelector('.carousel-inner')
    let carrousel_indicators = document.querySelector('.carousel-indicators')
    carrousel_inner_div.innerHTML = ``
    products.forEach((product, index) => {
        if(index === 0){
            carrousel_inner_div.insertAdjacentHTML('beforeend', 
            `<div class="carousel-item active">
                <img class="d-block w-100" src="${product.image}" alt="">
                <div class="carousel-caption d-none d-md-block">
                    <h4>${product.name}</h4>
                </div>
            </div>`
            );
            carrousel_indicators.insertAdjacentHTML('beforeend',
            ` <li data-target="#carouselExampleIndicators" data-slide-to="${index}" class="active"></li>

            `) 
        }else{
            carrousel_inner_div.insertAdjacentHTML('beforeend', 
            `<div class="carousel-item">
                <img class="carousel-img" src="${product.image}" alt="">
                <div class="carousel-caption d-none d-md-block">
                    <h4>${product.name}</h4>
                </div>
            </div>`
            );
            carrousel_indicators.insertAdjacentHTML('beforeend',
            ` <li data-target="#carouselExampleIndicators" data-slide-to="${index}"></li>
            `);  
        }
    });
};

const renderProducts = (products) => {
    console.log('render product function', products)
    const products_row = document.getElementById('product-details');
    products.forEach((product) => {
        products_row.innerHTML += `
        <div class="col-lg-3 col-md-6 col-sm-4">
            <a href="product/${product.id}"><img style="object-fit: cover" id='img-atag ${product.id}' class="img-thumbnail" src='${product.image}'></a>
            <div class="box-element product">
                <h6 class="pt-2" style="display: inline-block">${product.name.length > 20 ? product.name.slice(0,20).concat("...") : product.name}</h6>
                <span>Add</span>
               ${!product.sold_by_weight ? `<h6>precio p/u: <span class='float-right'><strong>$ ${product.price}</strong></span></h6>` : `<h6>Producto Vendio Por Peso<h6/>`} 	
            </div><br>
        </div>
        `
    });
}

const updateProducts = (products) => {
    let product_list = products.products
    let new_list = []
    if(products.has_more){
        if(!localStorage.getItem('products')){
            localStorage.setItem('products', JSON.stringify(product_list))
            new_list = products
        }else{
            console.log(JSON.parse(localStorage.getItem('products')))
            new_list = [... JSON.parse(localStorage.getItem('products')), ...product_list]
            localStorage.setItem('products', JSON.stringify(new_list))
        }
        
    renderProducts(product_list)

    }else{
        console.log('productos terminados')
    }
};

const buildMostPouplarProductsList = () => {
    const url = '/api/popular-products/'

    fetch(url)
        .then(function(response){ return response.json() })
        .then(fetchMostPopularProducts)
    };

const buildProductsList = () => {
    const url = '/api/product-list/'

    fetch(url)
        .then(function(response) { return response.json(); })
        .then(updateProducts);

    };

localStorage.setItem('limit', JSON.stringify(8))
localStorage.setItem('offset', JSON.stringify(0))
localStorage.removeItem('products')

const loadProducts = () => {
    let limit = JSON.parse(localStorage.getItem('limit'))
    let offset = JSON.parse(localStorage.getItem('offset'))

    const url = `/api/product-infinite/?limit=${limit}&offset=${offset}&/`
    fetch(url)

        .then(function(response){ return response.json() })
        .then(updateProducts) 
}

loadProducts()
buildMostPouplarProductsList()

window.addEventListener('scroll', () => {
        var scrollHeight = $(document).height();
        var scrollPos = $(window).height() + $(window).scrollTop();
    if(!((scrollHeight - 300) >= scrollPos)){
        let offset = JSON.parse(localStorage.getItem('offset'))
        let limit = JSON.parse(localStorage.getItem('limit'))
        localStorage.setItem('offset', JSON.stringify(offset + limit))
        loadProducts()
    }
});
