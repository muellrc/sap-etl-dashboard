# sap-pm-dashboard-odata
A sample project reading SAP PM Data (currently Equipments and Functional Locations) via OData and displaying the data in a Grafana Dashboard.

![Screenshot](https://user-images.githubusercontent.com/89973885/173239962-687ff44c-a79a-4856-8bd5-7351998c724a.png)


## How to Run

To run this project, simply call docker-compose:<br />

**Step 1:** docker-compose build <br />
**Step 2:** docker-compose up <br />
**Step 3:** Monitor the status updates from Prefect until the final workflow is executed and the message is shown:  <br />

```
INFO - prefect.FlowRunner | Flow run SUCCESS: all reference tasks succeeded
```
<br />

**Step 4:** Open the Grafana dashboard in http://127.0.0.1:8080/d/0GaKs2C7k/sap-pm-data-dashboard-equipments-and-functional-locations?orgId=1


## Components:

The following containers are used to provide the functionality described above:

- postgres-db: Container based on a standard postgres Docker image

- etl: Container based on a standard Python Docker image with the Prefect module used to build pipelines of batch jobs installed during provisioning along with other prerequisites.

- grafana: Container based on a standard Grafana Docker image, with a dashboard called "SAP PM Data Dashboard" provisioned via Dockerfile.
