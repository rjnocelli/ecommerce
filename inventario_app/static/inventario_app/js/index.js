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
    console.log('render product function')
    const products_row = document.getElementById('product-details');
    products.forEach((product) => {
        products_row.innerHTML += `
        <div class="col-lg-3 col-md-6 col-sm-4">
            <a href="product/${product.id}"><img id='img-atag ${product.id}' class="img-thumbnail" src="${product.image}"></a>
            <div class="box-element product">
                <h6 class="pt-2" style="display: inline-block">${product.name.length > 20 ? product.name.slice(0,20).concat("...") : product.name}</h6>
                <h6>precio p/u: <span class='float-right'><strong>$ ${product.price}</strong></span></h6><hr>		
                <a id='lo-quiero ${product.id}' class="btn btn-success btn-block btn-sm lo-quiero-button shadow-none" href="">Lo Quiero! <span class='far fa-candy-cane'></span></a>
            </div>
            <br>
        </div>
        `
    });
}

const updateProducts = (products) => {
    localStorage.setItem('products', JSON.stringify(products))
    
    renderProducts(products)
    addLoQuieroTag(products, "lo-quiero")
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

buildProductsList()
buildMostPouplarProductsList()

