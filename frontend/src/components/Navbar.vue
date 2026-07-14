<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm sticky-top">

        <div class="container-fluid">

            <router-link
                class="navbar-brand fw-bold"
                to="/"
            >
                PPA
            </router-link>

            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarNav"
            >
                <span class="navbar-toggler-icon"></span>
            </button>

            <div
                class="collapse navbar-collapse"
                id="navbarNav"
            >

                <ul class="navbar-nav">

                    <!-- STUDENT -->

                    <template v-if="role==='student'">

                        <li class="nav-item">
                            <router-link class="nav-link" to="/student/dashboard">
                                Dashboard
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <router-link
                                class="nav-link"
                                :class="{active:isProfile}"
                                to="/student/profile"
                            >
                                Profile
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <router-link
                                class="nav-link"
                                :class="{active:isDrives}"
                                to="/student/drives"
                            >
                                Available Drives
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <router-link
                                class="nav-link"
                                :class="{active:isApplications}"
                                to="/student/applications"
                            >
                                Applications
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <router-link
                                class="nav-link"
                                :class="{active:isOffers}"
                                to="/student/offers"
                            >
                                Offers
                            </router-link>
                        </li>

                    </template>



                    <!-- COMPANY -->

                    <template v-if="role==='company'">

                        <li class="nav-item">
                            <router-link class="nav-link" to="/company/dashboard">
                                Dashboard
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <router-link
                                class="nav-link"
                                :class="{active:isProfile}"
                                to="/company/profile"
                            >
                                Profile
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <router-link
                                class="nav-link"
                                :class="{active:isDrives}"
                                to="/company/drives"
                            >
                                Placement Drives
                            </router-link>
                        </li>

                    </template>



                    <!-- ADMIN -->

                    <template v-if="role==='admin'">

                        <li class="nav-item">
                            <router-link class="nav-link" to="/admin/dashboard">
                                Dashboard
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <router-link
                                class="nav-link"
                                :class="{active:isStudents}"
                                to="/admin/students"
                            >
                                Students
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <router-link
                                class="nav-link"
                                :class="{active:isCompanies}"
                                to="/admin/companies"
                            >
                                Companies
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <router-link
                                class="nav-link"
                                :class="{active:isAdminDrives}"
                                to="/admin/drives"
                            >
                                Drives
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <router-link
                                class="nav-link"
                                :class="{active:isAdminApplications}"
                                to="/admin/applications"
                            >
                                Applications
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <router-link
                                class="nav-link"
                                :class="{active:isHistory}"
                                to="/admin/placement-history"
                            >
                                Placement History
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <router-link
                                class="nav-link"
                                :class="{active:isStatistics}"
                                to="/admin/statistics"
                            >
                                Statistics
                            </router-link>
                        </li>

                    </template>



                    <li class="nav-item">

                        <a
                            href="#"
                            class="nav-link"
                            @click.prevent="logout"
                        >
                            Logout
                        </a>

                    </li>

                </ul>

            </div>

        </div>

    </nav>
</template>

<script>

export default{

    props:["role"],

    computed:{

        path(){
            return this.$route.path
        },

        isProfile(){
            return this.path.includes("/profile")
        },

        isDrives(){
            return this.path.includes("/drives") ||
                   this.path.includes("/drive/")
        },

        isApplications(){
            return this.path.includes("/applications")
        },

        isOffers(){
            return this.path.includes("/offers")
        },

        isStudents(){
            return this.path.includes("/admin/student")
        },

        isCompanies(){
            return this.path.includes("/admin/company")
        },

        isAdminDrives(){
            return this.path.includes("/admin/drive")
        },

        isAdminApplications(){
            return this.path.includes("/admin/applications")
        },

        isHistory(){
            return this.path.includes("/placement-history")
        },

        isStatistics(){
            return this.path.includes("/statistics")
        }

    },

    methods:{

        logout(){

            localStorage.removeItem("token")

            this.$router.push("/login")

        }

    }

}

</script>

<style scoped>

.navbar{

    min-height:65px;

}

.navbar-brand{

    font-size:24px;

    margin-right:30px;

}

.nav-link{

    color:white !important;

    margin-right:12px;

}

.nav-link.active{

    color:#ffc107 !important;

    font-weight:bold;

}

</style>