<template>
  <div v-if="error" class="error">{{error}}</div>
  <div v-if="products.length" class="products-list">
    <div v-for="product in products" :key='product.name' class="product thin-border">
      <div>
        <router-link :to="{ name:'detail', params:{id:product.id}}">
          <img v-if="product.image" :src="'data:image/png;base64,'+product.image" alt="Product Image">
          <img v-else src='/bundle/static/assets/images/product/default.png' alt="Product Image">
        </router-link>
      </div>
      <div class="label-product">
        <router-link :to="{ name:'detail', params:{id:product.id}}" class="product-link">
          {{ product.name }}
        </router-link>
        <div>
          $ {{product.price}}
        </div>
      </div>
    </div>
   
  </div>
  <div v-else>
    <Spinner/>
  </div>
   <div class="under-pagination">
      <Pagination @change-pagination="load"/>
    </div>
</template>

<script>
import { ref } from 'vue'
import Spinner from './Spinner.vue'
import Pagination from './Pagination.vue'
import { useRoute } from 'vue-router'
export default {
  components: { Spinner, Pagination },
  setup(){
    const route = useRoute()
    const error = ref(null)
    const products = ref([])
    const load = async ()=>{
      try{
        let data = await fetch('https://odoo.website/bundle/api/page/'+route.params.page)
                          .then(res => res.json())
        products.value = data.products
      }
      catch(err){
        error.value = err.message
      }
    }
    load()

    return {load,products,error}
  }
}
</script>

<style scoped>
  .products-list{
    margin:30px 20%;
    display: grid;
    grid-template-columns: auto auto auto auto;
  }

  .product{
    position: relative;
    justify-content: center;
    margin: 10px;
    padding: 20px 20px 60px;
  }

  .product:hover{
    box-shadow: 0 0 20px 0 rgb(0 0 0 / 10%);
  }

  .product:hover .label-product{
    background:#E9ECEF; 
  }

  .product img{
    width: 100%;
    height: 100%;
  }

  .product .label-product{
    width: 100%;
    left: 0;
    bottom: 0;
    padding: 10px 0 15px;
    position: absolute;
    text-align: center;
  }

  .product-link{
    display: inline-block;
    color: #267372;
    margin-bottom: 8px;
  }

  .product:nth-child(1){
    grid-area: 1/1/3/3;
  }

  .under-pagination{
    display: flex;
    justify-content: center;
    padding-bottom: 20px;
  }
</style>