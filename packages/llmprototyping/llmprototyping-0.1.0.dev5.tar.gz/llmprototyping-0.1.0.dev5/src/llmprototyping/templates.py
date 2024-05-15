from .llm_interface import Message
from .error import LLMPException

class Template:
    def __init__(self, name, metadata, text):
        self.name = name
        self.metadata = metadata
        # escape simple keys
        text = text.replace('{', '{{').replace('}', '}}')
        # double keys to simple
        text = text.replace('{{{{', '{').replace('}}}}', '}')
        self.text = text

    def render(self, context):
        return self.text.format(**context)

    def render_to_message(self, context):
        text = self.render(context)
        role = self.metadata.get('role','user')
        return Message(content = text, role = role)

class TemplateFileRepository:
    def __init__(self, filepath = None):
        self.templates = {}
        if filepath is not None:
            self.load_templates(filepath)

    def load_templates(self, filepath):
        current_template = None
        metadata = {}
        template_text = []
        reading_text = False

        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('# template: '):
                    if current_template:
                        self.templates[current_template] = Template(current_template, metadata, ''.join(template_text).strip())
                    current_template = ':'.join(line.split(':')[1:]).strip()
                    metadata = {}
                    template_text = []
                    reading_text = False
                elif line.startswith('#'):
                    x = line[1:].split(':')
                    key = x[0].strip()
                    value = ':'.join(x[1:]).strip()
                    metadata[key] = value
                else:
                    reading_text = True
                    line = line.replace('\\#','#')
                    template_text.append(line + '\n')

        if current_template:
            self.templates[current_template] = Template(current_template, metadata, ''.join(template_text).strip())

    def get_template(self, name):
        try:
            template = self.templates[name]
            return template
        except KeyError:
            raise LLMPException.not_found(f"template not found: {name}")

    def render_message(self, template_name, message_context):
        template = self.get_template(name = template_name)
        message = template.render_to_message(message_context)
        return message
