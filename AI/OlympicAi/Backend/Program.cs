using Scalar.AspNetCore;
using AI_spotter.Controllers;
using Microsoft.AspNetCore.Http.Features;
var builder = WebApplication.CreateBuilder(args);

// Increase the max size of body
builder.Services.Configure<FormOptions>(options =>
{
    options.MultipartBodyLengthLimit = 100 * 1024 * 1024; // Set limit to 100 MB
});

// also increases the max size of body
builder.WebHost.ConfigureKestrel(options =>
{
    options.Limits.MaxRequestBodySize = 100 * 1024 * 1024; // Set limit to 100 MB
});

builder.Services.AddHttpClient<IAiClientConnect, AiClientConnect>();
// Add services to the container.
builder.Services.AddControllers();
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    app.MapScalarApiReference();
}

//app.UseHttpsRedirection();


// app.UseAuthorization();

app.MapControllers();

app.Run();
