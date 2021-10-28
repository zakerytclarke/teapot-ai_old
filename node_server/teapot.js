import wordnet from 'wordnet';
import util from "util";
const wordnet_lookup=util.promisify(wordnet.lookup);


class TEAPOT{
    constructor(){
        this.KNOWLEDGE={
            john:{
                is:"old"
            },
            library:{
                open:"8am",
                close:"5pm"
            }
        };
    }
    
    async reply(txt){
       
        var parsed = await parse(txt);
        

        return parsed;
    }    


}


async function parse(txt){
    var words = txt.split(" ");

    var mappedWords = Promise.all(words.map(x=>getWordRecord(x)));



    return mappedWords;
}


async function getWordRecord(word){
    var out;

    var modifiedWord = word.toLowerCase();

    try{//Try wordnet lookup
        var definition = await wordnet_lookup(modifiedWord);


        out={
            word:word,
            lemma:modifiedWord,
            part_of_speech:definition[0].meta.synsetType

        };
    }catch(e){
        return {};
    }
    
    return out;
    
}


test();


async function test(){
    var tea = new TEAPOT();
    var response = await tea.reply("John is an old man who lives downtown.");
    console.log(response);
}