<script>
export default {
    data() {
        return {
            briefs: null,
            new_brief_title: '',
            new_brief_url: '',
            new_brief_nb_apprs: '',
            cur_brief_title: '',
            cur_brief_url: '',
            cur_brief_nb_apprs: '',
            messages: [],
            msg_class: "success_msg",
            sav_nb_apprs: '',
            force : {}
        }
    },
    methods: {
        clearMessages(){
            this.messages = []
        },
        async fetchBriefs() {
            console.log("Fetching Briefs")
            const res = await fetch(
                `http://127.0.0.1:8000/api/briefs/`
            )
            this.briefs = await res.json()
        },
        hide_all() {
            console.log(`Will hide all update forms`)
            this.briefs.forEach(brief => {
                console.log(`f_update_${brief.id}`)
                this.$refs[`f_update_${brief.id}`][0].style.display = 'none'
            });
        },
        async addBrief() {
            fetch("http://127.0.0.1:8000/api/briefs/", {
                method: "post",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },

                //make sure to serialize your JSON body
                body: JSON.stringify({
                    "brief_title": this.new_brief_title,
                    "brief_url": this.new_brief_url,
                    "brief_nb_apprs": this.new_brief_nb_apprs
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
                    this.messages.push(`Brief ${result.brief_title} ajouté avec succès!`)
                    this.msg_class = "succes_msg"
                    this.hide_all()
                    this.fetchBriefs()
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        },
        async updateBrief(brief_id) {
            fetch(`http://127.0.0.1:8000/api/briefs/${brief_id}/`, {
                method: "PATCH",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },

                //make sure to serialize your JSON body
                body: JSON.stringify({
                    "brief_title": this.cur_brief_title,
                    "brief_url": this.cur_brief_url,
                    "brief_nb_apprs": this.cur_brief_nb_apprs
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
                    if (this.sav_nb_apprs != result.brief_nb_apprs) {
                        this.force[result.id] = 1
                    }
                    this.messages.push(`Brief ${result.brief_title} mis à jour avec succès!`)
                    this.msg_class = "succes_msg"
                    this.hide_all()
                    this.fetchBriefs()
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            })
        },
        async deleteBrief(brief_id, brief_title) {
            if(confirm(`Voulez vous vraiment supprimer ${brief_title} ?`)){
                fetch(`http://127.0.0.1:8000/api/briefs/${brief_id}/`, {
                    method: "DELETE",
                })
                .then( (response) => {
                    this.clearMessages()
                    if (response.status == 204) {
                        this.messages.push(`Brief supprimé avec succès!`)
                        this.msg_class = "succes_msg"
                        this.hide_all()
                        this.fetchBriefs()
                    } else {
                        throw Error(response.statusText);
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                })
            }
        },
        async createGroup(brief_id) {
            fetch(`http://127.0.0.1:8000/api/briefs/gen_groups/${brief_id}`, {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({"force":this.force[brief_id]})
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
                if (result["error"]){
                    this.messages.push(`Groupes déjà créés pour ce brief!`)
                    this.msg_class = "err_msg"
                    this.hide_all()
                    this.fetchBriefs()                    
                } else {
                    this.messages.push(`Groupes créés avec succès!`)
                    this.msg_class = "succes_msg"
                    delete this.force[brief_id]
                    this.hide_all()
                    this.fetchBriefs()
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            })        
        },
        show(brief_id) {
            console.log(`Will display appr #${brief_id} update form`)
            this.briefs.forEach(brief => {
                console.log(`f_update_${brief.id}`)
                this.$refs[`f_update_${brief.id}`][0].style.display = 'none'
                if (brief.id == brief_id){
                    this.cur_brief_title = brief.brief_title
                    this.cur_brief_url = brief.brief_url
                    this.cur_brief_nb_apprs = brief.brief_nb_apprs
                    this.sav_nb_apprs = brief.brief_nb_apprs
                }
            });
            this.$refs[`f_update_${brief_id}`][0].style.display = 'block'
        },
    },
    mounted() {
        this.fetchBriefs()
    }
}
</script>

<template>
    <div>
        <v-list-item :class="msg_class">
            <v-list-item-content v-for="message in this.messages">
                {{ message }}
            </v-list-item-content>
        </v-list-item>

        <p v-if="!briefs">Loading...</p>
        <v-list v-else>
            <v-list-item 
                v-for="(brief,i) in this.briefs"
                v:key="i">
                <v-list-item-content>
                    <v-list-item-title v-text="brief.brief_title"></v-list-item-title>
                    <a href="#" @click="createGroup(brief.id)">Créer Groupes</a> |&nbsp;
                    <a href="#" @click="show(brief.id)">Modifier</a> |&nbsp;
                    <a href="#" @click="deleteAppr(brief.id, brief.brief_title)">Supprimer</a>
                    <br>
                    <form style="display: none;" :ref="'f_update_' + brief.id" @submit.prevent="updateBrief(brief.id)">
                        <v-container>
                            <v-text-field v-model="cur_brief_title" label="Title"></v-text-field>
                            <v-text-field v-model="cur_brief_url" label="URL"></v-text-field>
                            <v-text-field v-model="cur_brief_nb_apprs" label="Nombre d'apprenants"></v-text-field>
                            <v-btn @click="updateBrief(brief.id)">Mettre à jour</v-btn>
                        </v-container>
                    </form>
                </v-list-item-content>
                <v-list-item-content v-if="(brief.groups.length==0)">
                    <v-list-item-title>Les groupes pour ce brief n'ont pas été encore créés</v-list-item-title>
                </v-list-item-content>
                <v-list-item-content v-else>
                    <v-list-item 
                        v-for="(group,i) in brief.groups"
                        v:key="i">
                        <v-list-item-content>
                            <v-list-item-title v-text="group.grp_nom"></v-list-item-title>
                            <v-list-item 
                                v-for="(appr,i) in group.grp_apprs"
                                v:key="i">
                                <v-list-item-content>
                                    <v-list-item-title v-text="appr.appr_prenom +' '+ appr.appr_nom"></v-list-item-title>
                                </v-list-item-content>
                            </v-list-item>
                        </v-list-item-content>
                    </v-list-item>
                </v-list-item-content>
            </v-list-item>
        </v-list>
        <br>
        <h2>Ajouter un brief</h2>
        <v-form @submit.prevent="addBrief">
            <v-container>
                <v-text-field v-model="new_brief_title" label="Title"></v-text-field>
                <v-text-field v-model="new_brief_url" label="URL"></v-text-field>
                <v-text-field v-model="new_brief_nb_apprs" label="Nombre d'apprenants"></v-text-field>
                <v-btn @click="addBrief">Ajouter</v-btn>
            </v-container>
        </v-form>
    </div>
</template>

<style>
.err_msg {
    color: red;
}
.succes_msg {
    color: green;
}
ul {
    list-style: none;
}
</style>