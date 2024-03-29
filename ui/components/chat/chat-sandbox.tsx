// build a chat confirmation form
// it has a message and two buttons to confirm or cancel
// the message is loaded as a prop

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { ToolInterface } from "./chat-board";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { useForm } from "react-hook-form";
import { useFieldArray } from "react-hook-form";
import exp from "constants";
import { type } from "os";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { use } from "react";

const toolFormSchema = z.object({
  name: z.string(),
  // tool_arguments is a record of strings,
  arguments: z.record(z.string()),
});

type ToolFormValues = typeof toolFormSchema;
type ChatSandboxProps = {
  tool: ToolInterface;
  onConfirm: (values: ToolFormValues) => Promise<void>;
  onCancel?: () => void;
};

const ChatSandbox = ({
  tool,
  onConfirm,
  onCancel = () => {},
}: ChatSandboxProps) => {

  const form = useForm<ToolFormValues>({
    resolver: zodResolver(toolFormSchema),
    defaultValues: {
      name: tool.name,
      arguments: tool.arguments
    } 
  });
  // create fields from the tool arguments
  const fields = Object.keys(tool.arguments).map((id) => {
    return {
      name: id,
      value: tool.arguments[id]
    }
  });

  const handleConfirm = async (values: ToolFormValues) => {
    onConfirm(values);
  }
  console.log(fields);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Run Tool</CardTitle>
        <CardDescription>Confirm to run tool</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-6">
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleConfirm)}
            className="space-y-2 w-full"
          >
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel htmlFor="tool_name">Tool name</FormLabel>
                  <FormControl>
                    <Input {...field} />
                  </FormControl>
                </FormItem>
              )}
            />
            {fields.map((field, index) => (
              <FormField
                control={form.control}
                name={field.name}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel htmlFor="tool_argument_name">{field.name}</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                  </FormItem>
                )}
              />
            ))}
            <Button type="submit">Confirm</Button>
            <Button variant="secondary" onClick={onCancel}>
              Cancel
            </Button> 
          </form>
        </Form>
      </CardContent>
    </Card>
  );
}

export default ChatSandbox;

