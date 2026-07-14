<template>
    <Navbar role="admin"/>
    
    <div class="container mt-5">

        <h2 class="text-center mb-4">
            Placement Statistics
        </h2>


        <Bar v-if="loaded" :data="chartData" />


    </div>
</template>


<script>
import Navbar from "../components/Navbar.vue"

import { Bar } from "vue-chartjs"


import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale
} from "chart.js"



ChartJS.register(

    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale

)



export default {


    components: {

        Bar,
        Navbar

    },



    data() {

        return {

            loaded: false,


            chartData: {

                labels: [],

                datasets: []

            }

        }

    },



    mounted() {

        this.loadStatistics()

    },



    methods: {


        async loadStatistics() {


            const response = await fetch(
                "http://127.0.0.1:5000/api/admin/statistics",
                {
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )



            const result = await response.json()



            if (result.success) {


                this.chartData = {


                    labels: result.statistics.companies,


                    datasets: [

                        {
                            label: "Applied",
                            data: result.statistics.applied,
                            backgroundColor: "#0d6efd"
                        },

                        {
                            label: "Selected",
                            data: result.statistics.selected,
                            backgroundColor: "#ffc107"
                        },

                        {
                            label: "Accepted",
                            data: result.statistics.accepted,
                            backgroundColor: "#198754"
                        }

                    ]

                }



                this.loaded = true

            }


        }

    }

}

</script>