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
                this.$refs[`detail${brief.id}`][0].style.display = 'none'
            });
            this.$refs.add_brief.style.display = 'none'
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
        showUpdate(brief_id) {
            this.clearMessages()
            console.log(`Will display appr #${brief_id} update form`)
            this.briefs.find(brief => {
                console.log(`f_update_${brief.id}`)
                if (brief.id == brief_id){
                    this.cur_brief_title = brief.brief_title
                    this.cur_brief_url = brief.brief_url
                    this.cur_brief_nb_apprs = brief.brief_nb_apprs
                    this.sav_nb_apprs = brief.brief_nb_apprs
                }
            });
            if (this.$refs[`f_update_${brief_id}`][0].style.display != 'block') {
                this.hide_all()
                this.$refs[`f_update_${brief_id}`][0].style.display = 'block'
            } else {
                this.hide_all()
            }
        },
        showAdd() {
            this.clearMessages()
            console.log(`Will display appr add form`)
            if (this.$refs.add_brief.style.display != 'block') {
                this.hide_all()
                this.$refs.add_brief.style.display = 'block'
            } else {
                this.hide_all()
            }
        },
        showBriefDetails(brief_id) {
            console.log(`Will display brief details #${brief_id}`)
            this.clearMessages()
            this.briefs.forEach(brief => {
                console.log(`f_update_${brief.id}`)
            });
            if (this.$refs[`detail${brief_id}`][0].style.display != 'block') {
                this.hide_all();
                this.$refs[`detail${brief_id}`][0].style.display = 'block'
            } else {
                this.hide_all()
            }
        }

    },
    mounted() {
        this.fetchBriefs()
    }
}
</script>

<template id="brief">
    <v-card class="surcard">
        <v-card-title>
            <span>Briefs</span>
        </v-card-title>
        <v-spacer></v-spacer>
        <v-card-action>
            <v-btn @click="showAdd()" icon>
                <v-icon>mdi-plus-box</v-icon>
            </v-btn>
        </v-card-action>   
    </v-card>
    <div style="display: none; width: 90%;" ref="add_brief">
        <v-form @submit.prevent="addBrief">
            <h2>Ajouter un brief</h2>
            <v-text-field v-model="new_brief_title" label="Title"></v-text-field>
            <v-text-field v-model="new_brief_url" label="URL"></v-text-field>
            <v-text-field v-model="new_brief_nb_apprs" label="Nombre d'apprenants"></v-text-field>
            <v-btn @click="addBrief">Ajouter</v-btn>
    </v-form>
    </div>
    
    <v-card id="msg" :class="msg_class" ref="msg" v-for="message in this.messages">
        <v-card-title>{{ message }}</v-card-title>
    </v-card>
    <div id="list" v-for="(brief, i) in this.briefs" :key="i">
        <v-card class="card">
            <v-card-title>
            <span>{{ brief.brief_title }}</span>
            </v-card-title>
            <v-spacer></v-spacer>
            <v-card-action>
                <v-btn @click="showBriefDetails(brief.id)" icon>
                    <v-icon>
                        mdi-eye
                    </v-icon>
                </v-btn>
                <v-btn @click="showUpdate(brief.id)" icon>
                    <v-icon>
                        mdi-pencil
                    </v-icon>
                </v-btn>
                <v-btn @click="deleteBrief(brief.id, brief.brief_title)" icon>
                <v-icon>
                    mdi-delete
                </v-icon>
                </v-btn>
            </v-card-action>               
        </v-card>
        <div style="display: none;" :ref="'detail' + brief.id" class="undercard">
            <v-card class="detailcard">
                <v-card-title class="detailtitle">Détails</v-card-title>
            </v-card>
            <v-card class="detailcard2">
                <v-card-title>
                    <span>URL:</span> {{brief.brief_url}} 
                </v-card-title>
                <v-card-title>
                    <span>Nombre d'apprenants:</span> {{brief.brief_nb_apprs}}
                </v-card-title>
            </v-card>
            <v-card class="detailcard">
                <v-card-title class="detailtitle">Groupes</v-card-title>
                <v-spacer></v-spacer>
                <v-card-action>
                    <v-btn @click="createGroup(brief.id)" icon>
                        <v-icon>
                            mdi-account-multiple-plus
                        </v-icon>
                    </v-btn>
                </v-card-action>
            </v-card>
            <v-card class="group" v-if="(brief.groups.length != 0)" v-for="(group,i) in brief.groups" :key="i">
                <v-card-title><span>{{ group.grp_nom}}</span></v-card-title>
                <v-card>
                    <v-card-title v-for="(appr,i) in group.grp_apprs" :key="i">
                        {{ appr.appr_prenom }} {{ appr.appr_nom }}
                    </v-card-title>
                </v-card>
            </v-card>
            <v-card class="group" v-else>
                <v-card-title>
                    Les groupes ne sont pas encores créés
                </v-card-title>
            </v-card>
        </div>
        <div style="display: none;" :ref="'f_update_' + brief.id" @submit.prevent="updateBrief(brief.id)">
            <v-form @submit.prevent="updateBrief(brief.id)">
                <v-text-field v-model="cur_brief_title"></v-text-field>
                <v-text-field v-model="cur_brief_url"></v-text-field>
                <v-text-field v-model="cur_brief_nb_apprs"></v-text-field>     
                <v-btn id="btn_form" @click="updateBrief(brief.id)">Mettre à jour</v-btn>            
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
.v-card.group {
    background-color: #e8e7dc;
    display: inline-block;
    margin: 1%;
    margin-left: 1.5%;
    vertical-align: top;
}
#msg {
    margin: 1%;
}
.v-card.detailcard {
    background-color: #e8e7dc;
    display: flex;
    margin: 1%;
    padding: 1%;
}
.v-card.detailcard2 {
    display: block;
    margin: 1.5%;
    padding: 1%;
}
.v-card-title.detailtitle{
    font-weight: bold;

}
.v-btn {
    margin-right: 10px;
}
#brief {
    display: flex;
}
#list {
    width: 90%;
}
.v-form {
    width: 90%;
    margin: 10px;
}
.undercard.v-card {
    width: 90%;
}
span {
    font-weight: bold;
}
</style>