var myBio = {
	"name": "Amish Patel",
	"role": "Software Developer",
	"contacts": {
		"email":"av2patel@uwaterloo.ca",
		"github": "amishpatel1994",
		"twitter": "@AmishP4tel",
		"location": "Mississauga, ON, Canada"
		},
	"welcomeMessage": 	"A keen interest in learning exciting new technologies especially the ones related to web!",
	"skills": ["Quick Learner", "Being Awesome", "Hard Worker", "Self Motivator", "Perseverence"],
	"bioPic":"https://scontent-a-ord.xx.fbcdn.net/hphotos-xap1/v/t1.0-9/s720x720/1972515_10152735581627040_3158059248618056471_n.jpg?oh=6dd6805cd6942dbba174871793f81bd2&oe=54FBBF4E",

};

var work = {
	"jobs": [
		{	"position": "Web Developer",
			"employer": "FarmLogs",
			"date": "January 2015 - April 2015",
			"description": "Building awesome web applications for farmers!",
			"location": "Ann Arbor, Michigan, US"
		},
		{
			"position": "Software Developer",
			"employer": "Ontario Institute for Cancer Research",
			"date": "May 2014 - August 2014",
			"description": "Directed the planning, design, and implementation of a console software that launches and provisions multiple clusters on various cloud environments such as AWS, vCloud, OpenStack, and VirtualBox simultaneously",
			"location": "Toronto, ON, Canada"
		}
	]
};

var project = {
	"projects": [
		{
			"name": "HELPR",
			"date": "May 2014 - August 2014",
			"description": "Android application which finds nearby voltuneer locations",
			"image": "https://lh5.ggpht.com/1DJJRN0Q-v8CQqGfwXzI-DIm3eQri6uaprpHtPOlHya4EMYA2X7dNb5YScSoesMmmkA=h900-rw"
		}
	]
};

var education = {
	"schools":[
		{	"name": "University of Waterloo",
			"years": "2012-2017",
			"location": "Waterloo, ON, Canada",
			"degree": "BASc",
			"major": "Computer Engineering"
		}
	],
	"onlineCourses":[
		{
			"name": "Udacity",
			"years": "2013-present",
			"location": "Internet",
			"degree": "Curiousity",
			"major": "CS"
		}
	]
};

displayHeader();
displayWork();
displayProject();
displayEducation();
$("#mapDiv").append(googleMap);



function displayEducation(){
	//the work section of the resume
	for (var i = 0; i < education.schools.length; i++){
		var formattedEduName = HTMLschoolName.replace("%data%", education.schools[i].name);
		var formattedEdudeg = HTMLschoolDegree.replace("%data%", education.schools[i].degree);
		var formattedEduYears = HTMLschoolDates.replace("%data%", education.schools[i].years);
		var formattedEduLocation = HTMLschoolLocation.replace("%data%", education.schools[i].location);
		var formattedEduMajor = HTMLschoolMajor.replace("%data%", education.schools[i].major);
		$("#education").append(HTMLschoolStart+formattedEduName+formattedEdudeg+formattedEduYears+formattedEduLocation+formattedEduMajor);
	}
}

function displayProject(){
	//the work section of the resume
	for (var i = 0; i < project.projects.length; i++){
		var formattedProjTitle = HTMLprojectTitle.replace("%data%", project.projects[i].name);
		var formattedProjDate = HTMLprojectDates.replace("%data%", project.projects[i].date);
		var formattedProjDesc = HTMLprojectDescription.replace("%data%", project.projects[i].description);
		var formattedProjImg = HTMLprojectImage.replace("%data%", project.projects[i].image);
		$("#projects").append(HTMLprojectStart+formattedProjTitle+formattedProjDate+formattedProjDesc+formattedProjImg);
	}
}


function displayHeader(){
	//header portion
	var formattedName = HTMLheaderName.replace("%data%", myBio.name);
	var formattedRole = HTMLheaderRole.replace("%data%", myBio.role);
	var formattedEmail = HTMLemail.replace("%data%", myBio.contacts.email);
	var formattedgithub = HTMLgithub.replace("%data%", myBio.contacts.github);
	var formattedtwitter = HTMLtwitter.replace("%data%", myBio.contacts.twitter);
	var formattedBioPic = HTMLbioPic.replace("%data%", myBio.bioPic);
	var formattedmsg = HTMLWelcomeMsg.replace("%data%", myBio.welcomeMessage);
	console.log(formattedName);
	$("#header").prepend(formattedName+formattedRole);
	$("#topContacts").append(formattedEmail+formattedgithub+formattedtwitter);
	$("#footerContacts").append(formattedEmail+formattedgithub+formattedtwitter);
	$("#header").append(formattedBioPic);
	$("#header").append(formattedmsg);
	if (myBio.skills.length > 0){
		var formattedSkills;
		$("#header").append(HTMLskillsStart);
		for (var i = 0; i < myBio.skills.length; i++){
			formattedSkills = HTMLskills;
			formattedSkills = formattedSkills.replace("%data%", myBio.skills[i]);
			$("#skills").append(formattedSkills);
		}
	}
}

function displayWork(){

	//the work section of the resume
	for (var i = 0; i < work.jobs.length; i++){
		var formattedEmployer = HTMLworkEmployer.replace("%data%", work.jobs[i].employer);
		var formattedJobTitle = HTMLworkTitle.replace("%data%", work.jobs[i].position);
		var formattedJobDates = HTMLworkDates.replace("%data%", work.jobs[i].date);
		var formattedJobLocation = HTMLworkLocation.replace("%data%", work.jobs[i].location);
		var formattedJobDescription = HTMLworkDescription.replace("%data%", work.jobs[i].description);
		console.log(formattedJobTitle+formattedEmployer);
		$("#workExperience").append(HTMLworkStart+formattedEmployer+formattedJobTitle+formattedJobDates+formattedJobLocation+formattedJobDescription);

	}

}