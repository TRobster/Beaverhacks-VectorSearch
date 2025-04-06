/*
 * Write your routing code in this file.  Make sure to add your name and
 * @oregonstate.edu email address below.
 *
 * Name:Chase Vanderlip
 * Email:vanderlc@oregonstate.edu
 *
 */

//notes to ask ta how to check if gitbash is on the engr servers to be able to use the address of engr servers to host 
//the homepage needs a header and post and will be the root and needs 

//404 needs a header 
//post page needs a header and a post

// var path = require('path')
var express = require('express')//need express handlebars 
var expresshandle = require('express-handlebars')


var postdata= require("./postData.json")

var app = express()
var port = process.env.PORT || 3000  //server port 3000

app.engine("handlebars", expresshandle.engine())

app.set("view engine","handlebars")//added
// app.set("views","./views")

app.use(express.static('static'))

//git command to add all
//git add --all

//another git command to push and add comment
// git commit -m "adding the handlebars"

//basic middleware function 
//comand is node server.js 
//ctrl c to stop program 
//hosted on local machine at http://localhost:3000 
// how to start program with npm start 
//another to install handlebars is npm install handlebars
// look at lecture for 11/20/2024 
// must make handlebars for filters,module and header
//need a views folder 
// another gitbash cammdn to go back is cd -
app.use(function (req, res, next ){//next is a call for the next middleware function 

    console.log("-- Request received")
    console.log(" --method:", req.method)
    console.log(" --method:", req.url)
    console.log(" --method:", req.headers)
    next()



    //next() allows a responce to go through
    //res.send(" ") send what html in ("") to server
    //res.status().send()
    //status code goes in status()
})

//test for static index.html .
app.get("/", function (req,res) {
    console.log("-- home page requested ")
    
    //res.status(200).sendFile(__dirname + "/static/index.html")
    //next()
    res.render("postpage",{
        posts: postdata,
        showFilter: true,
        showSellSomethingModal: true
    })


})

app.get('/posts/:posts',function(req,res, next){
    //parce through each post 
    //don't have to take operateing systems 2
    //to test use http://localhost:3000/posts/0
    var postid=req.params.posts;
    console.log(postid)
    if(postdata[postid]){
        res.status(200).render('postpage', {
            posts:[postdata[postid]]
        });
    }else {
        next();
    } 
    
     
    }); 






app.listen(port, function () {
    console.log("http://localhost:", port)

})


app.get('*', function (req, res) {
    res.status(404).render("404")


    //res.status(404).sendFile(path.join(__dirname, 'static', '404.html'))
})




// var avaliableposts=app.use(package.json())
//new code start 
//to have a function go through each post look at 11/25/2024
//another shortcut "ctrl a" to highlight everything 
// //post cantainer is nulll
// app.get('/post/:posts',function(req,res, next){


//     for(var i=0; i<postdata.length;i++){
//         res.render("Posts",postdata)

//     }

    // var posts=req.params.posts.toLowerCase()// used in video to grab from the person name 
    
    // if(avaliableposts.indexof(posts)>=0){
    //     res.render("Posts",postdata)
    // }
    
    // if()
    //   {{#each}}

    //   {{/each}}
    


// }) 

