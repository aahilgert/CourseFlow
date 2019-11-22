from rest_framework import serializers
from .models import (
    Course,
    Preparation,
    Activity,
    Assesment,
    Artifact,
    Strategy,
    Node,
    NodeStrategy,
    StrategyActivity,
    ComponentWeek,
    WeekCourse,
    Component,
    Week,
    Discipline,
    Outcome,
    OutcomeNode,
    OutcomeStrategy,
    OutcomePreparation,
    OutcomeActivity,
    OutcomeAssesment,
    OutcomeArtifact,
    OutcomeWeek,
    OutcomeCourse,
    User,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username"]


class OutcomeSerializer(serializers.ModelSerializer):

    author = UserSerializer(allow_null=True)

    class Meta:
        model = Outcome
        fields = [
            "id",
            "title",
            "description",
            "created_on",
            "last_modified",
            "hash",
            "author",
        ]

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

class OutcomeNodeSerializer(serializers.ModelSerializer):

    outcome = OutcomeSerializer(allow_null=True)

    class Meta:
        model = OutcomeNode
        fields = ["node", "outcome", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get('rank', instance.title)
        outcome_data = self.initial_data.pop('outcome')
        outcome_serializer = OutcomeSerializer(Outcome.objects.get(id=outcome_data['id']), outcome_data)
        outcome_serializer.is_valid()
        outcome_serializer.save()
        instance.save()
        return instance

class ParentNodeSerializer(serializers.ModelSerializer):

    author = UserSerializer(allow_null=True)

    class Meta:
        model = Node
        fields = [
            "id",
            "title",
            "description",
            "last_modified",
            "hash",
            "author",
            "work_classification",
            "activity_classification",
            "classification",
        ]

class ParentStrategySerializer(serializers.ModelSerializer):

    author = UserSerializer(allow_null=True)

    class Meta:
        model = Strategy
        fields = [
            "id",
            "title",
            "description",
            "last_modified",
            "hash",
            "author",
        ]


class NodeSerializer(serializers.ModelSerializer):

    author = UserSerializer(allow_null=True)

    outcomenode_set = serializers.SerializerMethodField()

    parent_node = ParentNodeSerializer(allow_null=True)


    class Meta:
        model = Node
        fields = [
            "id",
            "title",
            "description",
            "created_on",
            "last_modified",
            "hash",
            "author",
            "work_classification",
            "activity_classification",
            "classification",
            "outcomenode_set",
            "is_original",
            "parent_node",
        ]

    def get_outcomenode_set(self, instance):
        links = instance.outcomenode_set.all().order_by("rank")
        return OutcomeNodeSerializer(links, many=True).data

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.classification = validated_data.get('classification', instance.classification)
        instance.work_classification = validated_data.get('work_classification', instance.work_classification)
        instance.activity_classification = validated_data.get('activity_classification', instance.activity_classification)
        for outcomenode_data in self.initial_data.pop('outcomenode_set'):
            outcomenode_serializer = OutcomeNodeSerializer(OutcomeNode.objects.get(id=outcomenode_data['id']), data=outcomenode_data)
            outcomenode_serializer.is_valid()
            outcomenode_serializer.save()
        instance.save()
        return instance

class NodeStrategySerializer(serializers.ModelSerializer):

    node = NodeSerializer()

    class Meta:
        model = NodeStrategy
        fields = ["strategy", "node", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data['rank']
        node_data = self.initial_data.pop('node')
        node_serializer = NodeSerializer(Node.objects.get(id=node_data['id']), node_data)
        node_serializer.is_valid()
        node_serializer.save()
        instance.save()
        return instance

class OutcomeStrategySerializer(serializers.ModelSerializer):

    outcome = OutcomeSerializer()

    class Meta:
        model = OutcomeStrategy
        fields = ["strategy", "outcome", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get('rank', instance.title)
        outcome_data = self.initial_data.pop('outcome')
        outcome_serializer = OutcomeSerializer(Outcome.objects.get(id=outcome_data['id']), outcome_data)
        outcome_serializer.is_valid()
        outcome_serializer.save()
        instance.save()
        return instance

class StrategySerializer(serializers.ModelSerializer):

    author = UserSerializer(allow_null=True)

    nodestrategy_set = serializers.SerializerMethodField()

    outcomestrategy_set = serializers.SerializerMethodField()

    parent_strategy = ParentStrategySerializer(allow_null=True)

    class Meta:
        model = Strategy
        fields = [
            "id",
            "title",
            "description",
            "created_on",
            "last_modified",
            "hash",
            "default",
            "author",
            "nodestrategy_set",
            "outcomestrategy_set",
            "is_original",
            "parent_strategy",
        ]

    def get_nodestrategy_set(self, instance):
        links = instance.nodestrategy_set.all().order_by("rank")
        return NodeStrategySerializer(links, many=True).data

    def get_outcomestrategy_set(self, instance):
        links = instance.outcomestrategy_set.all().order_by("rank")
        return OutcomeStrategySerializer(links, many=True).data

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        for nodestrategy_data in self.initial_data.pop('nodestrategy_set'):
            nodestrategy_serializer = NodeStrategySerializer(NodeStrategy.objects.get(id=nodestrategy_data['id']), data=nodestrategy_data)
            nodestrategy_serializer.is_valid()
            nodestrategy_serializer.save()
        for outcomestrategy_data in self.initial_data.pop('outcomestrategy_set'):
            outcomestrategy_serializer = OutcomeStrategySerializer(OutcomeStrategy.objects.get(id=outcomestrategy_data['id']), data=outcomestrategy_data)
            outcomestrategy_serializer.is_valid()
            outcomestrategy_serializer.save()
        instance.save()
        return instance


class StrategyActivitySerializer(serializers.ModelSerializer):

    strategy = StrategySerializer()

    class Meta:
        model = StrategyActivity
        fields = ["activity", "strategy", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get('rank', instance.rank)
        strategy_data = self.initial_data.pop('strategy')
        strategy_serializer = StrategySerializer(Strategy.objects.get(id=strategy_data['id']), strategy_data)
        strategy_serializer.is_valid()
        strategy_serializer.save()
        instance.save()
        return instance

class OutcomeActivitySerializer(serializers.ModelSerializer):

    outcome = OutcomeSerializer()

    class Meta:
        model = OutcomeActivity
        fields = ["activity", "outcome", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get('rank', instance.title)
        outcome_data = self.initial_data.pop('outcome')
        outcome_serializer = OutcomeSerializer(Outcome.objects.get(id=outcome_data['id']), outcome_data)
        outcome_serializer.is_valid()
        outcome_serializer.save()
        instance.save()
        return instance


class ActivitySerializer(serializers.ModelSerializer):

    author = UserSerializer(allow_null=True)

    strategyactivity_set = serializers.SerializerMethodField()

    outcomeactivity_set = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            "id",
            "title",
            "description",
            "author",
            "created_on",
            "last_modified",
            "hash",
            "strategyactivity_set",
            "outcomeactivity_set",
        ]

    def get_strategyactivity_set(self, instance):
        links = instance.strategyactivity_set.all().order_by("rank")
        return StrategyActivitySerializer(links, many=True).data

    def get_outcomeactivity_set(self, instance):
        links = instance.outcomeactivity_set.all().order_by("rank")
        return OutcomeActivitySerializer(links, many=True).data

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        for strategyactivity_data in self.initial_data.pop('strategyactivity_set'):
            strategyactivity_serializer = StrategyActivitySerializer(StrategyActivity.objects.get(id=strategyactivity_data['id']), data=strategyactivity_data)
            strategyactivity_serializer.is_valid()
            strategyactivity_serializer.save()
        for outcomeactivity_data in self.initial_data.pop('outcomeactivity_set'):
            outcomeactivity_serializer = OutcomeActivitySerializer(OutcomeActivity.objects.get(id=outcomeactivity_data['id']), data=outcomeactivity_data)
            outcomeactivity_serializer.is_valid()
            outcomeactivity_serializer.save()
        instance.save()
        return instance


class OutcomePreparationSerializer(serializers.ModelSerializer):

    outcome = OutcomeSerializer()

    class Meta:
        model = OutcomeActivity
        fields = ["preparation", "outcome", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get('rank', instance.title)
        outcome_data = self.initial_data.pop('outcome')
        outcome_serializer = OutcomeSerializer(Outcome.objects.get(id=outcome_data['id']), outcome_data)
        outcome_serializer.is_valid()
        outcome_serializer.save()
        instance.save()
        return instance


class PreparationSerializer(serializers.ModelSerializer):

    author = UserSerializer(allow_null=True)

    outcomepreparation_set = serializers.SerializerMethodField()

    class Meta:
        model = Preparation
        fields = [
            "id",
            "title",
            "description",
            "author",
            "created_on",
            "last_modified",
            "hash",
            "outcomepreparation_set",
        ]

    def get_outcomepreparation_set(self, instance):
        links = instance.outcomepreparation_set.all().order_by("rank")
        return OutcomePreparationSerializer(links, many=True).data


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        for outcomepreparation_data in self.initial_data.pop('outcomepreparation_set'):
            outcomepreparation_serializer = OutcomePreparationSerializer(OutcomePreparation.objects.get(id=outcomepreparation_data['id']), data=outcomepreparation_data)
            outcomepreparation_serializer.is_valid()
            outcomepreparation_serializer.save()
        instance.save()
        return instance

class OutcomeAssesmentSerializer(serializers.ModelSerializer):

    outcome = OutcomeSerializer()

    class Meta:
        model = OutcomeAssesment
        fields = ["assesment", "outcome", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get('rank', instance.title)
        outcome_data = self.initial_data.pop('outcome')
        outcome_serializer = OutcomeSerializer(Outcome.objects.get(id=outcome_data['id']), outcome_data)
        outcome_serializer.is_valid()
        outcome_serializer.save()
        instance.save()
        return instance


class AssesmentSerializer(serializers.ModelSerializer):

    author = UserSerializer(allow_null=True)

    outcomeassesment_set = serializers.SerializerMethodField()

    class Meta:
        model = Assesment
        fields = [
            "id",
            "title",
            "description",
            "author",
            "created_on",
            "last_modified",
            "hash",
            "outcomeassesment_set",
            ]

    def get_outcomeassesment_set(self, instance):
        links = instance.outcomeassesment_set.all().order_by("rank")
        return OutcomeAssesmentSerializer(links, many=True).data


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        for outcomeassesment_data in self.initial_data.pop('outcomeassesment_set'):
            outcomeassesment_serializer = OutcomeAssesmentSerializer(OutcomeAssesment.objects.get(id=outcomeassesment_data['id']), data=outcomeassesment_data)
            outcomeassesment_serializer.is_valid()
            outcomeassesment_serializer.save()
        instance.save()
        return instance


class OutcomeArtifactSerializer(serializers.ModelSerializer):

    outcome = OutcomeSerializer()

    class Meta:
        model = OutcomeArtifact
        fields = ["artifact", "outcome", "added_on", "rank", "id"]


    def update(self, instance, validated_data):
        instance.rank = validated_data.get('rank', instance.title)
        outcome_data = self.initial_data.pop('outcome')
        outcome_serializer = OutcomeSerializer(Outcome.objects.get(id=outcome_data['id']), outcome_data)
        outcome_serializer.is_valid()
        outcome_serializer.save()
        instance.save()
        return instance


class ArtifactSerializer(serializers.ModelSerializer):

    author = UserSerializer(allow_null=True)

    outcomeartifact_set = serializers.SerializerMethodField()

    class Meta:
        model = Artifact
        fields = [
            "id",
            "title",
            "description",
            "author",
            "created_on",
            "last_modified",
            "hash",
            "outcomeartifact_set",
        ]

    def get_outcomeartifact_set(self, instance):
        links = instance.outcomeartifact_set.all().order_by("rank")
        return OutcomeArtifactSerializer(links, many=True).data


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        for outcomeartifact_data in self.initial_data.pop('outcomeartifact_set'):
            outcomeartifact_serializer = OutcomeArtifactSerializer(OutcomeArtifact.objects.get(id=outcomeartifact_data['id']), data=outcomeartifact_data)
            outcomeartifact_serializer.is_valid()
            outcomeartifact_serializer.save()
        instance.save()
        return instance


class ComponentSerializer(serializers.ModelSerializer):

    content_object = serializers.SerializerMethodField()

    content_type = serializers.SerializerMethodField()

    class Meta:
        model = Component
        fields = ["content_object", "content_type", "id"]

    def get_content_object(self, instance):
        if type(instance.content_object) == Activity:
            return ActivitySerializer(instance.content_object).data
        elif type(instance.content_object) == Preparation:
            return PreparationSerializer(instance.content_object).data
        elif type(instance.content_object) == Assesment:
            return AssesmentSerializer(instance.content_object).data
        else:
            return ArtifactSerializer(instance.content_object).data

    def get_content_type(self, instance):
        if type(instance.content_object) == Activity:
            return 0
        elif type(instance.content_object) == Preparation:
            return 1
        elif type(instance.content_object) == Assesment:
            return 2
        else:
            return 3

    def update(self, instance, validated_data):
        content_object_data = self.initial_data.pop('content_object')
        if type(instance.content_object) == Activity:
            content_object_serializer = ActivitySerializer(Activity.objects.get(id=content_object_data['id']), data=content_object_data)
        elif type(instance.content_object) == Preparation:
            content_object_serializer = PreparationSerializer(Preparation.objects.get(id=content_object_data['id']), data=content_object_data)
        elif type(instance.content_object) == Assesment:
            content_object_serializer = AssesmentSerializer(Assesment.objects.get(id=content_object_data['id']), data=content_object_data)
        else:
            content_object_serializer = ArtifactSerializer(Artifact.objects.get(id=content_object_data['id']), data=content_object_data)
        content_object_serializer.is_valid()
        content_object_serializer.save()
        instance.save()
        return instance


class ComponentWeekSerializer(serializers.ModelSerializer):

    component = ComponentSerializer()

    class Meta:
        model = ComponentWeek
        fields = ["week", "component", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get('rank', instance.rank)
        component_data = self.initial_data.pop('component')
        component_serializer = ComponentSerializer(Component.objects.get(id=component_data['id']), component_data)
        component_serializer.is_valid()
        component_serializer.save()
        instance.save()
        return instance

class OutcomeWeekSerializer(serializers.ModelSerializer):

    outcome = OutcomeSerializer()

    class Meta:
        model = OutcomeWeek
        fields = ["week", "outcome", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get('rank', instance.title)
        outcome_data = self.initial_data.pop('outcome')
        outcome_serializer = OutcomeSerializer(Outcome.objects.get(id=outcome_data['id']), outcome_data)
        outcome_serializer.is_valid()
        outcome_serializer.save()
        instance.save()
        return instance


class WeekSerializer(serializers.ModelSerializer):

    componentweek_set = serializers.SerializerMethodField()

    author = UserSerializer(allow_null=True)

    outcomeweek_set = serializers.SerializerMethodField()

    class Meta:
        model = Week
        fields = [
            "id",
            "title",
            "hash",
            "created_on",
            "last_modified",
            "author",
            "componentweek_set",
            "outcomeweek_set",
        ]

    def get_componentweek_set(self, instance):
        links = instance.componentweek_set.all().order_by("rank")
        return ComponentWeekSerializer(links, many=True).data

    def get_outcomeweek_set(self, instance):
        links = instance.outcomeweek_set.all().order_by("rank")
        return OutcomeWeekSerializer(links, many=True).data


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        for componentweek_data in self.initial_data.pop('componentweek_set'):
            componentweek_serializer = ComponentWeekSerializer(ComponentWeek.objects.get(id=componentweek_data['id']), data=componentweek_data)
            componentweek_serializer.is_valid()
            componentweek_serializer.save()
        for outcomeweek_data in self.initial_data.pop('outcomeweek_set'):
            outcomeweek_serializer = OutcomeWeekSerializer(OutcomeWeek.objects.get(id=outcomeweek_data['id']), data=outcomeweek_data)
            outcomeweek_serializer.is_valid()
            outcomeweek_serializer.save()
        instance.save()
        return instance




class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ["id", "title"]


class WeekCourseSerializer(serializers.ModelSerializer):

    week = WeekSerializer()

    class Meta:
        model = WeekCourse
        fields = ["course", "week", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get('rank', instance.rank)
        week_data = self.initial_data.pop('week')
        week_serializer = WeekSerializer(Week.objects.get(id=week_data['id']), week_data)
        week_serializer.is_valid()
        week_serializer.save()
        instance.save()
        return instance


class OutcomeCourseSerializer(serializers.ModelSerializer):

    outcome = OutcomeSerializer()

    class Meta:
        model = OutcomeCourse
        fields = ["course", "outcome", "added_on", "rank", "id"]

    def update(self, instance, validated_data):
        instance.rank = validated_data.get('rank', instance.title)
        outcome_data = self.initial_data.pop('outcome')
        outcome_serializer = OutcomeSerializer(Outcome.objects.get(id=outcome_data['id']), outcome_data)
        outcome_serializer.is_valid()
        outcome_serializer.save()
        instance.save()
        return instance


class CourseSerializer(serializers.ModelSerializer):

    weekcourse_set = serializers.SerializerMethodField()

    author = UserSerializer(allow_null=True)

    discipline = DisciplineSerializer(allow_null=True)

    outcomecourse_set = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "author",
            "created_on",
            "last_modified",
            "hash",
            "weekcourse_set",
            "outcomecourse_set",
            "discipline",
        ]

    def get_weekcourse_set(self, instance):
        links = instance.weekcourse_set.all().order_by("rank")
        return WeekCourseSerializer(links, many=True).data

    def get_outcomecourse_set(self, instance):
        links = instance.outcomecourse_set.all().order_by("rank")
        return OutcomeCourseSerializer(links, many=True).data


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        for weekcourse_data in self.initial_data.pop('weekcourse_set'):
            weekcourse_serializer = WeekCourseSerializer(WeekCourse.objects.get(id=weekcourse_data['id']), data=weekcourse_data)
            weekcourse_serializer.is_valid()
            weekcourse_serializer.save()
        for outcomecourse_data in self.initial_data.pop('outcomecourse_set'):
            outcomecourse_serializer = OutcomeCourseSerializer(OutcomeCourse.objects.get(id=outcomecourse_data['id']), data=outcomecourse_data)
            outcomecourse_serializer.is_valid()
            outcomecourse_serializer.save()
        instance.save()
        return instance
