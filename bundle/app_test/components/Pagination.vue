<template>
  <div class="pagination mx-4 flex">
        <div @click="prev" class="pagination-button eraser-border-right thin-border prev-button pointer">Prev</div>
        <div v-for="i in 2" :key="i">
            <router-link :to="{name:'shopPage',params:{page:i}}" class="pagination-button eraser-border-right thin-border">{{i}}</router-link>
        </div>
        <div @click="next" class="pagination-button thin-border next-button pointer">Next</div>
    </div>
</template>

<script>
import { onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
export default {
    setup(){
        const route = useRoute()
        const router = useRouter()

        var page = reactive(route.params.page)
        const prev = () =>{
            if(page!=1){
                page--;
                router.push({name:'shopPage',params:{page:page}})
            }
        }
        const next = () =>{
            if(page!=2){
                router.push({name:'shopPage',params:{page:++page}})    
            }
        }
        return {prev,next,onMounted}
    },
    watch: {
        $route () {
            this.$emit('change-pagination')
        }
    }
}
</script>

<style scoped>
.eraser-border-right{
    border-right: none !important;
}
.pagination-button{
  padding: 9px 12px;
  color: var(--mini-button);
}

.prev-button{
    border-top-left-radius: 3px;
    border-bottom-left-radius: 3px;
}

.next-button{
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
}

.pagination a{
    display: block;
}

.pagination .router-link-active{
    color: white ;
    background: var(--mini-button);
}



</style>