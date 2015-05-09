#include "rapidjson/prettywriter.h" // for stringify JSON
#include "rapidjson/filereadstream.h"
#include "rapidjson/document.h"     // rapidjson's DOM-style API
#include <cstdio>

using namespace rapidjson;

int main(int argc, char** argv)
{
    if(argc < 2){
        printf("Usage: %s json_file\n\n", argv[0]);
        return -1;
    }

    FILE* fp = fopen(argv[1], "r");

    char readBuffer[65535];
    FileReadStream is(fp, readBuffer, sizeof(readBuffer));

    Document d;
    d.ParseStream(is);

    fclose(fp);

    //将读取的json重新格式化输出
    printf("\nModified JSON with reformatting:\n");
    StringBuffer sb;
    PrettyWriter<StringBuffer> writer(sb);
    d.Accept(writer);    // Accept() traverses the DOM and generates Handler events.
    puts(sb.GetString());

    printf("\n\n");

    //解析json,生成配置相关的map
    
    printf("*********************\n");

    static const char* kTypeNames[] = 
            {"Null", "False", "True", "Object", "Array", "String", "Number"};
    for(Value::ConstMemberIterator it = d.MemberBegin(); it != d.MemberEnd(); ++it) {
        const char* name = it->name.GetString();
        const char* type_name = kTypeNames[it->value.GetType()];
        printf("name:%s valueType:%s\n", name, type_name);
        if(strcmp(type_name, "String") == 0) {
            printf("\tname:%s value:%s\n", name, it->value.GetString());
        }
        else if(strcmp(type_name, "Number") == 0) {
            printf("\tname:%s value:%d\n", name, it->value.GetInt());
        }
        else if(strcmp(type_name, "Array") == 0){
            const Value& values = it->value;
            for(Value::ConstValueIterator itr=values.Begin(); itr != values.End(); ++itr) {
                if(strcmp(kTypeNames[itr->value.GetType()], "String") == 0){
                    printf("%s : %s\n", itr->name.GetString(), itr->value.GetString());
                }
                else if(strcmp(kTypeNames[itr->value.GetType()], "Number") == 0){
                    printf("%s : %d\n", itr->name.GetString(), itr->value.GetInt());
                }
            }


        }

    }
    //assert(d.HasMember("keyname"));

    ////get keyname
    //const Value& key = d["keyname"];
    //assert(key.IsString());

    //const char* key_name = key.GetString();

    //printf("key:%s\n", key_name);

    ////read values
    //const Value& values = d["values"];
    //assert(values.IsArray());

    //printf("values size is:%d\n", values.Size());
    //for(Value::ConstValueIterator it=values.Begin(); it != values.End(); ++it) {
        //assert(it->IsObject());
        //查找实际的key
        //
        //Value::ConstMemberIterator itr = it->FindMember(key_name);
        //if(itr != it->MemberEnd()){
            //printf("%s : %d\n", itr->name.GetString(), itr->value.GetInt());
        //}
    //}

    return 0;
}


