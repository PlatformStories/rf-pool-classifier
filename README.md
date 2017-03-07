# rf-pool-classifier

A GBDX task that trains a random forest classifier to classify polygons of arbitrary geometry into those that contain swimming pools and those that do not.


## Run

Here we run a sample execution of the rf-pool-classifier task. Sample inputs are provided on S3 in the locations specified below.

1. In a Python terminal create a GBDX interface and specify the task input location:

    ```python
    from gbdxtools import Interface
    from os.path import join
    import uuid

    gbdx = Interface()

    input_location = 's3://gbd-customer-data/58600248-2927-4523-b44b-5fec3d278c09/platform-stories/rf-pool-classifier/'
    ```

2. Create a task instance and set the required inputs:

    ```python
    rf_task = gbdx.Task('rf-pool-classifier')
    rf_task.inputs.image = join(input_location, 'image')
    rf_task.inputs.geojson = join(input_location, 'geojson')
    rf_task.inputs.n_estimators = "1000"
    ```

3. Create a single-task workflow object and define where the output data should be saved.

    ```python
    workflow = gbdx.Workflow([rf_task])
    random_str = str(uuid.uuid4())
    output_location = join('platform-stories/trial-runs', random_str)

    workflow.savedata(rf_task.outputs.trained_classifier, output_location)
    ```

4. Execute the workflow and monitor its status as follows:

    ```python
    workflow.execute()
    workflow.status
    ```

## Input Ports

GBDX input ports can only be of "Directory" or "String" type. Booleans, integers and floats are passed to the task as strings, e.g., "True", "10", "0.001".

| Name  | Type | Description | Required |
|---|---|---|---|
| image | directory | Contains the image strip where the polygons are found. | True |
| geojson | directory | Contains a geojson with labeled polygons. Each polygon has the properties feature_id, image_id, and class_name (either 'No swimming pool' or 'Swimming pool') | True |
| n_estimators | string | Number of trees to use in the random forest classifier. Defaults to 100. | False |

## Output Ports

| Name  | Type | Description |
|---|---|---|
| trained_classifier | directory | Contains the file 'classifier.pkl' which is the trained random forest classifier. |


## Development

### Build the Docker Image

You need to install [Docker](https://docs.docker.com/engine/installation).

Clone the repository:

```bash
git clone https://github.com/platformstories/rf-pool-classifier
```

Then

```bash
cd rf-pool-classifier
docker build -t rf-pool-classifier .
```

### Try out locally

Create a container in interactive mode and mount the sample input under `/mnt/work/input/`:

```bash
docker run --rm -v full/path/to/sample-input:/mnt/work/input -it rf-pool-classifier
```

Then, within the container:

```bash
python /rf-pool-classifier.py
```

### Docker Hub

Login to Docker Hub:

```bash
docker login
```

Tag your image using your username and push it to DockerHub:

```bash
docker tag rf-pool-classifier yourusername/rf-pool-classifier
docker push yourusername/rf-pool-classifier
```

The image name should be the same as the image name under containerDescriptors in rf-pool-classifier.json.

Alternatively, you can link this repository to a [Docker automated build](https://docs.docker.com/docker-hub/builds/). Every time you push a change to the repository, the Docker image gets automatically updated.
### Register on GBDX

In a Python terminal:
```python
from gbdxtools import Interface
gbdx=Interface()
gbdx.task_registry.register(json_filename="rf-pool-classifier-definition.json")
```

Note: If you change the task image, you need to reregister the task with a higher version number in order for the new image to take effect. Keep this in mind especially if you use Docker automated build.
