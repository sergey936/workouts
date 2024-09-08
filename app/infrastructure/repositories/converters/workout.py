from domain.entities.workout import Workout
from domain.values.workout import Text, Title
from infrastructure.db.models.workout import WorkoutModel


def convert_workout_entity_to_db_model(workout: Workout) -> WorkoutModel:
    return WorkoutModel(
        id=workout.oid,
        trainer_id=workout.trainer_oid,
        title=workout.title.as_generic_type(),
        description=workout.description.as_generic_type(),
        file_url=workout.file_path,
        is_active=workout.is_active
    )


def convert_db_model_to_workout_entity(workout: WorkoutModel) -> Workout:
    return Workout(
        oid=workout.id,
        trainer_oid=workout.trainer_id,
        title=Title(workout.title),
        description=Text(workout.description),
        file_path=workout.file_url,
        is_active=workout.is_active,
        price=workout.price
    )
