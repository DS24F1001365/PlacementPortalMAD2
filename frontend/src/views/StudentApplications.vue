<template>

<div class="container mt-5">

    <h2 class="text-center mb-4">

        My Applications

    </h2>

    <div v-if="success">

        <table class="table table-bordered table-striped">

            <thead>

                <tr>

                    <th>Company</th>
                    <th>Role</th>
                    <th>Specialization</th>
                    <th>Application Status</th>
                    <th>Drive Status</th>

                </tr>

            </thead>

            <tbody>

                <tr
                    v-for="application in applications"
                    :key="application.id"

                    :class="{

                        'table-danger':application.drive_status=='Cancelled',

                        'table-warning':application.drive_status=='Closed'

                    }"
                >

                    <td>

                        {{ application.company }}

                    </td>

                    <td>

                        {{ application.job_title }}

                    </td>

                    <td>

                        {{ application.specialization }}

                    </td>

                    <td>

                        {{ application.application_status }}

                    </td>

                    <td>

                        {{ application.drive_status }}

                    </td>

                </tr>

            </tbody>

        </table>

    </div>

    <div v-else>

        <div class="alert alert-danger">

            {{ message }}

        </div>

    </div>

</div>

</template>

<script>

export default{

    data(){

        return{

            success:false,

            message:"",

            applications:[]

        }

    },

    mounted(){

        this.loadApplications()

    },

    methods:{

        async loadApplications(){

            const response=await fetch(

                "http://127.0.0.1:5000/api/student/applications",

                {

                    headers:{

                        "Authorization":"Bearer "+localStorage.getItem("token")

                    }

                }

            )

            const result=await response.json()

            if(result.success){

                this.success=true

                this.applications=result.applications

            }

            else{

                this.message=result.message

            }

        }

    }

}

</script>