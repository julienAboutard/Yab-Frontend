<script>
export default {
    data() {
        return {
            apprenants: null,
            new_appr_nom: '',
            new_appr_prenom: '',
            cur_appr_nom: '',
            cur_appr_prenom: '',
            messages: [],
            msg_class: "success_msg"
        }
    },
    methods: {
        clearMessages(){
            this.messages = []
        },
        async fetchApprs() {
            console.log("Fetching apprenants")
            const res = await fetch(
                `http://127.0.0.1:8000/api/apprenants/`
            )
            this.apprenants = await res.json()
        },
        hide_all() {
            console.log(`Will hide all update forms`)
            this.apprenants.forEach(appr => {
                console.log(`f_update_${appr.id}`)
                this.$refs[`f_update_${appr.id}`][0].style.display = 'none'
            });
            this.$refs.add_appr.style.display = 'none'
        },
        async addAppr() {
            fetch("http://127.0.0.1:8000/api/apprenants/", {
                method: "post",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },

                //make sure to serialize your JSON body
                body: JSON.stringify({
                    "appr_nom": this.new_appr_nom,
                    "appr_prenom": this.new_appr_prenom
                })
            })
            .then( (response) => {
                this.clearMessages()
                if ((response.status > 200 && response.status < 300) || response.status == 400) {
                    return new Promise((resolve) => response.json()
                        .then((result) => resolve({
                        status: response.status,
                        result,
                    })));
                } else {
                    throw Error(response.statusText);
                }
            })
            .then(({status, result}) => {
                console.log("Result: ", result)
                console.log("Status: ", status)
                if (status == 400){
                    for (const [key, value] of Object.entries(result)) {
                        this.messages.push(`Erreur pour le champ ${key}: ${value}`)
                    }
                    this.msg_class = "err_msg"
                } else {  // 200
                    this.messages.push(`Apprenant ${result.appr_prenom} ${result.appr_nom} ajouté avec succès!`)
                    
                    this.msg_class = "succes_msg"
                    this.hide_all()
                    this.fetchApprs()
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        },
        async updateAppr(appr_id) {
            fetch(`http://127.0.0.1:8000/api/apprenants/${appr_id}/`, {
                method: "PATCH",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },

                //make sure to serialize your JSON body
                body: JSON.stringify({
                    "appr_nom": this.cur_appr_nom,
                    "appr_prenom": this.cur_appr_prenom
                })
            })
            .then( (response) => {
                this.clearMessages()
                if (response.status == 200 || response.status == 400) {
                    return new Promise((resolve) => response.json()
                        .then((result) => resolve({
                        status: response.status,
                        result,
                    })));
                } else {
                    throw Error(response.statusText);
                }
            })
            .then(({status, result}) => {
                console.log("Result: ", result)
                console.log("Status: ", status)
                if (status == 400){
                    for (const [key, value] of Object.entries(result)) {
                        this.messages.push(`Erreur pour le champ ${key}: ${value}`)
                    }
                    this.msg_class = "err_msg"
                } else {  // 200
                    this.messages.push(`Apprenant ${result.appr_prenom} ${result.appr_nom} mis à jour avec succès!`)
                    
                    this.msg_class = "succes_msg"
                    this.hide_all()
                    this.fetchApprs()
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            })
        },
        async deleteAppr(appr_id, appr_nom, appr_prenom) {
            if(confirm(`Voulez vous vraiment supprimer ${appr_nom} ${appr_prenom} ?`)){
                fetch(`http://127.0.0.1:8000/api/apprenants/${appr_id}/`, {
                    method: "DELETE",
                })
                .then( (response) => {
                    this.clearMessages()
                    if (response.status == 204) {
                        this.messages.push(`Apprenant supprimé avec succès!`)
                        
                        this.msg_class = "succes_msg"
                        this.hide_all()

                        this.fetchApprs()
                    } else {
                        throw Error(response.statusText);
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                })
            }
        },
        async show(appr_id) {
            this.clearMessages()
            this.apprenants.find(appr => {
                if (appr.id == appr_id){
                    this.cur_appr_nom = appr.appr_nom
                    this.cur_appr_prenom = appr.appr_prenom
                }
            });
            if (this.$refs[`f_update_${appr_id}`][0].style.display != 'block') {
                this.hide_all() 
                this.$refs[`f_update_${appr_id}`][0].style.display = 'block'
            } else {
                this.hide_all()
            }
            
            
        },
        showAdd() {
            this.clearMessages()
            console.log(`Will display appr add form`)
            if (this.$refs.add_appr.style.display != 'block') {
                this.hide_all()
                this.$refs.add_appr.style.display = 'block'
            } else {
                this.hide_all()
            }
            
        }

    },
    mounted() {
        this.fetchApprs()
    }
}
</script>

<template id="appr">
    <v-card class="surcard">
        <v-card-title>
            <span>Apprenants</span>
        </v-card-title>
        <v-spacer></v-spacer>
        <v-card-action>
            <v-btn @click="showAdd()" icon>
                <v-icon>mdi-plus-box</v-icon>
            </v-btn>
        </v-card-action>   
    </v-card>
    <div style="display: none; width: 90%;" ref="add_appr">
        <v-form @submit.prevent="addAppr">
            <h2>Ajouter un apprenant</h2>
            <v-text-field v-model="new_appr_prenom" label="Prénom"></v-text-field>
            <v-text-field v-model="new_appr_nom" label="Nom"></v-text-field>
            <v-btn @click="addAppr">Ajouter</v-btn>
        </v-form>
    </div>
    <v-card :class="msg_class" ref="msg" v-for="message in this.messages">
        <v-card-title>{{ message }}</v-card-title>
    </v-card>
    <div id="list" v-for="(appr, i) in this.apprenants" :key="i">
        <v-card class="card">
            <v-card-title>
            <span>{{ appr.appr_prenom }} {{ appr.appr_nom }}</span>
            </v-card-title>
            <v-spacer></v-spacer>
            <v-card-action>
                <v-btn @click="show(appr.id)" icon>
                    <v-icon>
                        mdi-pencil
                    </v-icon>
                </v-btn>
                <v-btn @click="deleteAppr(appr.id, appr.appr_prenom, appr.appr_nom)" icon>
                <v-icon>
                    mdi-delete
                </v-icon>
                </v-btn>
            </v-card-action>               
        </v-card>
        <div style="display: none;" :ref="'f_update_' + appr.id">
            <v-form>
                <v-text-field v-model="cur_appr_prenom"></v-text-field>
                <v-text-field v-model="cur_appr_nom"></v-text-field>            
                <v-btn id="btn_form" @click="updateAppr(appr.id)">Mettre à jour</v-btn>            
            </v-form>
        </div>
    </div>
</template>

<style>
.err_msg {
    color: red;
}
.succes_msg {
    color: green;
}
.v-card.card {
    background-color: #e8e7dc;
    display: flex;
    padding-top: 1%;
    padding-bottom: 1%;
    margin-bottom: 1%;
}
.v-card.surcard {
    background-color: #59B984;
    display: flex;
    width: 90%;
    padding-top: 1%;
    padding-bottom: 1%;
    margin-bottom: 1%;
    margin-top: 0.5%;
}

.v-btn {
    margin-right: 10px;
}
#appr {
    display: flex;
}
#list {
    width: 90%;
}
.v-form {
    width: 90%;
    margin: 10px;
    padding: 1%;
}

</style>