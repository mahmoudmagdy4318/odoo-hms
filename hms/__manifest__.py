{
    'name':"hms module",
    'summary':"module for patients",

    'depends':[
        'crm'
    ],
    'data':[
        "security/hms_groups.xml",
        "security/ir.model.access.csv",
        "views/hms_patient.xml",
        "views/hms_departments.xml",
        "views/hms_doctors.xml",
        "views/hms_logs.xml",
        "views/customers.xml",
        "reports/report.xml",
        "reports/hms_template.xml"
    ],
    # "images":['img/footer.jpeg',],
}