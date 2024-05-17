# Re-export benchling_sdk.models benchling_sdk such that
# users can import from benchling_sdk without exposing benchling_api_client.
#
# Do not write by hand. Run `poetry run task models` to generate.
# This file should be committed as part of source control.


import sys
from typing import TYPE_CHECKING

__all__ = [
    "AppActivateRequestedWebhookV2",
    "AppActivateRequestedWebhookV2Type",
    "AppDeactivatedWebhookV2",
    "AppDeactivatedWebhookV2Type",
    "CanvasInitializeWebhookV0",
    "CanvasInitializeWebhookV0Type",
    "CanvasInitializeWebhookV2",
    "CanvasInitializeWebhookV2Type",
    "CanvasInteractionWebhookV0",
    "CanvasInteractionWebhookV0Type",
    "CanvasInteractionWebhookV2",
    "CanvasInteractionWebhookV2Type",
    "LifecycleActivateWebhookV0",
    "LifecycleActivateWebhookV0Type",
    "LifecycleDeactivateWebhookV0",
    "LifecycleDeactivateWebhookV0Type",
    "MessageBaseV0",
    "WebhookEnvelopeV0",
    "WebhookEnvelopeV0App",
    "WebhookEnvelopeV0AppDefinition",
    "WebhookEnvelopeV0Version",
    "WebhookMessageV0",
]

if TYPE_CHECKING:
    import benchling_api_client.webhooks.v0.stable.models.app_activate_requested_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.app_activate_requested_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.app_deactivated_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.app_deactivated_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v0
    import benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v0_type
    import benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v0
    import benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v0_type
    import benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v2
    import benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v2_type
    import benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0
    import benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0_type
    import benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0
    import benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0_type
    import benchling_api_client.webhooks.v0.stable.models.message_base_v0
    import benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0
    import benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_app
    import benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_app_definition
    import benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_version
    import benchling_api_client.webhooks.v0.stable.models.webhook_message_v0

    AppActivateRequestedWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.app_activate_requested_webhook_v2.AppActivateRequestedWebhookV2
    )
    AppActivateRequestedWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.app_activate_requested_webhook_v2_type.AppActivateRequestedWebhookV2Type
    )
    AppDeactivatedWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.app_deactivated_webhook_v2.AppDeactivatedWebhookV2
    )
    AppDeactivatedWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.app_deactivated_webhook_v2_type.AppDeactivatedWebhookV2Type
    )
    CanvasInitializeWebhookV0 = (
        benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v0.CanvasInitializeWebhookV0
    )
    CanvasInitializeWebhookV0Type = (
        benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v0_type.CanvasInitializeWebhookV0Type
    )
    CanvasInitializeWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v2.CanvasInitializeWebhookV2
    )
    CanvasInitializeWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v2_type.CanvasInitializeWebhookV2Type
    )
    CanvasInteractionWebhookV0 = (
        benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v0.CanvasInteractionWebhookV0
    )
    CanvasInteractionWebhookV0Type = (
        benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v0_type.CanvasInteractionWebhookV0Type
    )
    CanvasInteractionWebhookV2 = (
        benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v2.CanvasInteractionWebhookV2
    )
    CanvasInteractionWebhookV2Type = (
        benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v2_type.CanvasInteractionWebhookV2Type
    )
    LifecycleActivateWebhookV0 = (
        benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0.LifecycleActivateWebhookV0
    )
    LifecycleActivateWebhookV0Type = (
        benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0_type.LifecycleActivateWebhookV0Type
    )
    LifecycleDeactivateWebhookV0 = (
        benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0.LifecycleDeactivateWebhookV0
    )
    LifecycleDeactivateWebhookV0Type = (
        benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0_type.LifecycleDeactivateWebhookV0Type
    )
    MessageBaseV0 = benchling_api_client.webhooks.v0.stable.models.message_base_v0.MessageBaseV0
    WebhookEnvelopeV0 = benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0.WebhookEnvelopeV0
    WebhookEnvelopeV0App = (
        benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_app.WebhookEnvelopeV0App
    )
    WebhookEnvelopeV0AppDefinition = (
        benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_app_definition.WebhookEnvelopeV0AppDefinition
    )
    WebhookEnvelopeV0Version = (
        benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_version.WebhookEnvelopeV0Version
    )
    WebhookMessageV0 = benchling_api_client.webhooks.v0.stable.models.webhook_message_v0.WebhookMessageV0

else:
    model_to_module_mapping = {
        "AppActivateRequestedWebhookV2": "benchling_api_client.webhooks.v0.stable.models.app_activate_requested_webhook_v2",
        "AppActivateRequestedWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.app_activate_requested_webhook_v2_type",
        "AppDeactivatedWebhookV2": "benchling_api_client.webhooks.v0.stable.models.app_deactivated_webhook_v2",
        "AppDeactivatedWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.app_deactivated_webhook_v2_type",
        "CanvasInitializeWebhookV0": "benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v0",
        "CanvasInitializeWebhookV0Type": "benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v0_type",
        "CanvasInitializeWebhookV2": "benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v2",
        "CanvasInitializeWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.canvas_initialize_webhook_v2_type",
        "CanvasInteractionWebhookV0": "benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v0",
        "CanvasInteractionWebhookV0Type": "benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v0_type",
        "CanvasInteractionWebhookV2": "benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v2",
        "CanvasInteractionWebhookV2Type": "benchling_api_client.webhooks.v0.stable.models.canvas_interaction_webhook_v2_type",
        "LifecycleActivateWebhookV0": "benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0",
        "LifecycleActivateWebhookV0Type": "benchling_api_client.webhooks.v0.stable.models.lifecycle_activate_webhook_v0_type",
        "LifecycleDeactivateWebhookV0": "benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0",
        "LifecycleDeactivateWebhookV0Type": "benchling_api_client.webhooks.v0.stable.models.lifecycle_deactivate_webhook_v0_type",
        "MessageBaseV0": "benchling_api_client.webhooks.v0.stable.models.message_base_v0",
        "WebhookEnvelopeV0": "benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0",
        "WebhookEnvelopeV0App": "benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_app",
        "WebhookEnvelopeV0AppDefinition": "benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_app_definition",
        "WebhookEnvelopeV0Version": "benchling_api_client.webhooks.v0.stable.models.webhook_envelope_v0_version",
        "WebhookMessageV0": "benchling_api_client.webhooks.v0.stable.models.webhook_message_v0",
    }

    from types import ModuleType

    # Custom module to allow for lazy loading of models
    class _Models(ModuleType):
        def __getattr__(self, name):
            module = __import__(model_to_module_mapping[name], None, None, [name])
            setattr(self, name, getattr(module, name))
            return ModuleType.__getattribute__(self, name)

    # keep a reference to this module so that it's not garbage collected
    old_module = sys.modules[__name__]

    new_module = sys.modules[__name__] = _Models(__name__)
    new_module.__dict__.update(
        {
            "__file__": __file__,
            "__path__": __path__,
            "__doc__": __doc__,
            "__all__": __all__,
        }
    )
