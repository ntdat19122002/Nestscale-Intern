<template>
  <div class="nav-search">
        <div class="search mx-4">
            <input type="text" name="" id="" placeholder="Search..." class="thin-border">
            <div class="mini-button search-button">
                <i class="fa fa-search"></i>
            </div>
        </div>
        <div class="currency price-list pp-button mx-4">Public Pricelist</div>
        <Pagination @change-pagination="load"/>
        <div class="type mx-4">
            <i class="fas fa-th-large pp-button" @click="makeType" :class="{typeActive:isGrid}"></i>
            <i class="fa-sharp fa-solid fa-list-ul pp-button"  @click="makeType" :class="{typeActive:!isGrid}"></i>
        </div>
        <div class="sort pp-button mx-4">Sort by</div>
    </div>
</template>

<script>
import { ref } from 'vue'
import Pagination from './Pagination.vue'
export default {
  components: { Pagination },
  setup(){
    const isGrid = ref(true);
    const makeType = (e) => {
        if (!e.target.classList.contains("typeActive")) {
            isGrid.value = !isGrid.value
        }
    }
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

    return{isGrid,makeType,load}
  }
}
</script>
<style scoped>

.nav-search{
  margin-top: 8px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
}


.fa-th-large{
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}

.fa-list-ul{
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}
.typeActive{
  background: rgb(96, 78, 91);
}
</style>