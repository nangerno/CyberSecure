from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

class SearchMitre(TemplateView):
    template_name = 'neograph/search_mitre.html'

    @method_decorator(login_required, name='dispatch')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search MITRE'  # Set the title for the template
        context['groupIcons'] = {
                "attack-pattern": "/static/neograph/image/icon/stix2_attack_pattern_icon_tiny_round_v1.png",
                "course-of-action": "/static/neograph/image/icon/stix2_course_of_action_icon_tiny_round_v1.png",
                "intrusion-set": "/static/neograph/image/icon/stix2_intrusion_set_icon_tiny_round_v1.png",
                "malware": "/static/neograph/image/icon/stix2_malware_icon_tiny_round_v1.png",
                "identity": "/static/neograph/image/icon/stix2_identity_icon_tiny_round_v1.png",
                "tool": "/static/neograph/image/icon/stix2_tool_icon_tiny_round_v1.png",
                "campaign": "/static/neograph/image/icon/stix2_campaign_icon_tiny_round_v1.png",           
                "x-mitre-data-source": "/static/neograph/image/icon/stix2_campaign_icon_tiny_round_v1.png",           
                "x-mitre-data-component": "/static/neograph/image/icon/stix2_campaign_icon_tiny_round_v1.png",           
            }
        return context
