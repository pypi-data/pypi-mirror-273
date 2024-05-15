from typing import List

from persona_ai.constants import TERMINATION_TOKEN
from persona_ai.domain.conversations import Message, MessageBody
from persona_ai.domain.tasks import Task
from persona_ai.models.base import GenAIModel
from persona_ai.moderation.ai_moderator import AIModerator
from persona_ai.moderation.base import ModerationResult, Rule
from persona_ai.prompts.base import Prompt
from persona_ai.prompts.jinja import JinjaTemplatePrompt
from persona_ai.prompts.utils import (
    render_context,
    get_context,
    get_task_history,
    render_conversation_history,
)
from persona_ai.tools.base import ToolDefinition
from persona_ai.transport.messagebus import Participant


class HistoryModerator(AIModerator):
    """
    This moderator uses history to select the next participant.
    """

    refine_request = False
    """
    If True, the moderator will create a question for the next participant.
    """

    fallback_participant: Participant | None = None
    """
    If no participant is found, the moderator will select this participant.
    """

    include_final_answer: bool = False
    """
    If True, the final answer should be included in the moderation.
    """

    def __init__(
        self,
        model: GenAIModel = None,
        rules: List[Rule] = None,
        prompt: Prompt = None,
        refine_request=False,
        fallback_participant: Participant | None = None,
        include_final_answer: bool = False,
    ):
        super().__init__(model=model, rules=rules)
        self.refine_request = refine_request
        self.fallback_participant = fallback_participant
        self.prompt = (
            prompt if prompt else JinjaTemplatePrompt(template="history_moderator")
        )
        self.include_final_answer = include_final_answer

    def _process_response(
        self, allowed_participants: List[Participant], response: MessageBody, task: Task
    ):
        if not response.tool_suggestion:
            if self.fallback_participant:
                return ModerationResult(
                    next=self.fallback_participant,
                    reason="Fallback participant selected",
                    request=None,
                    final_answer_found=False,
                )
            else:
                return ModerationResult(
                    next=None,
                    reason="No participant found",
                    final_answer_found=True,
                    final_answer=response.text,
                )
        tool_suggestion = response.tool_suggestion
        next_participant = tool_suggestion.input.get("participant_id", "UNKNOWN")
        reason = tool_suggestion.input.get("thought", "UNKNOWN")
        request_for_next_participant = tool_suggestion.input.get(
            "participant_question", None
        )
        participant = next(
            filter(lambda p: p.id == next_participant, allowed_participants),
            None,
        )

        final_answer_found = next_participant == TERMINATION_TOKEN

        final_answer = None
        if "final_answer" in tool_suggestion.input:
            final_answer = tool_suggestion.input["final_answer"]

        if self.fallback_participant and not final_answer_found:
            if not participant and task.is_first_iteration():
                return ModerationResult(
                    next=self.fallback_participant,
                    reason="Fallback participant selected",
                    request=None,
                    final_answer_found=False,
                )

        return ModerationResult(
            next=participant,
            reason=reason,
            request=request_for_next_participant if self.refine_request else None,
            final_answer_found=final_answer_found,
            final_answer=final_answer or None,
        )

    def _create_next_tool(
        self, allowed_participants: List[Participant], include_final_anwser=False
    ):
        definition = ToolDefinition(
            name="set_next_participant",
            description="Sets the next participant.",
            schema={
                "type": "object",
                "properties": {
                    "participant_id": {
                        "type": "string",
                        "enum": [TERMINATION_TOKEN]
                        + [x.id for x in allowed_participants],
                        "description": "The ID of the participant",
                    },
                    "thought": {
                        "type": "string",
                        "description": f"The reason why you choose this participant and your thoughts",
                    },
                    "participant_question": {
                        "type": "string",
                        "description": f"The question that moderator should ask to next participant to continue the conversation",
                    },
                },
                "required": ["participant_id", "thought", "participant_question"],
            },
        )

        if include_final_anwser:
            definition.schema["properties"]["final_answer"] = {
                "type": "string",
                "description": "The final answer of the conversation",
            }

        return definition

    def _render_prompt(
        self,
        allowed_participants,
        conversation_history,
        init_message: Message,
        task: Task,
    ):
        context = get_context(task, conversation_history)
        conversation_history = get_task_history(task, conversation_history)

        prompt = self.prompt.render(
            participants=allowed_participants,
            context=render_context(context),
            conversation_history=render_conversation_history(conversation_history),
            termination_token=TERMINATION_TOKEN,
            request=init_message.get_text(),
        )

        return prompt

    def _create_tools(self, allowed_participants):
        next_tool = self._create_next_tool(
            allowed_participants, self.include_final_answer
        )
        return [next_tool]
